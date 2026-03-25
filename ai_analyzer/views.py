from django.shortcuts import render
import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from applications.models import JobApplication
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class AnalyzeResumeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            app = JobApplication.objects.get(pk=pk, user=request.user)
        except JobApplication.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        job_description = request.data.get('job_description') or app.job_description

        if not job_description:
            return Response({'error': 'Job description is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not app.resume:
            return Response({'error': 'No resume uploaded for this application'}, status=status.HTTP_400_BAD_REQUEST)

        # Read resume text from PDF
        resume_text = extract_pdf_text(app.resume.path)

        prompt = f"""
You are an expert ATS (Applicant Tracking System) and career coach.

Analyze the following resume against the job description and return a JSON object with exactly these fields:
{{
  "match_score": <integer 0-100>,
  "matched_keywords": [<list of keywords from job description found in resume>],
  "missing_keywords": [<list of important keywords from job description missing in resume>],
  "suggestions": [<list of 3-5 specific, actionable improvement suggestions>],
  "overall_summary": "<2-3 sentence summary of the match>"
}}

Return ONLY the JSON object, no extra text.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        raw = response.choices[0].message.content.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        feedback = json.loads(raw.strip())

        # Save feedback to application
        app.job_description = job_description
        app.ai_feedback = feedback
        app.save()

        return Response(feedback, status=status.HTTP_200_OK)


def extract_pdf_text(path: str) -> str:
    try:
        import pypdf
        text = ""
        with open(path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        return f"Could not extract PDF text: {str(e)}"