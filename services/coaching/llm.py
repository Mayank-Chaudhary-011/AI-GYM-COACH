from services.config.workout_config import PROMPT


class LLMCoach:
    def __init__(self, groq_client=None):
        self.client = groq_client
        self.history = []
        self.system_prompt = PROMPT

    def give_feedback(self, event, issue):
        if not self.client:
            return self._fallback_feedback(event, issue)

        prompt = f"Event: {event}"

        if issue:
            prompt += f" Form Issue: {issue}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.history[-10:],
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.4,
        )

        text = response.choices[0].message.content.strip()
        self.history.append({"role": "assistant", "content": text})

        return text

    def _fallback_feedback(self, event, issue):
        if event == "workout_started":
            return "Let’s get started — stay strong and keep your form tight."
        if event == "set_completed":
            return "Great job! One set down, keep the momentum going."
        if event == "workout_completed":
            return "Nice work — the workout is complete, keep that energy up."
        if event == "no_pose_detected":
            return issue or "I can’t see you. Please move into the camera frame."

        if event == "ongoing_form_check":
            if issue:
                return issue
            return "Nice form — keep going and breathe steadily."

        return "Keep going — stay focused on your form."    