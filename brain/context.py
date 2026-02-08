class ConversationContext:
    def __init__(self):
        self.history = []

    def add(self, user, ai):
        self.history.append((user, ai))
        if len(self.history) > 4:
            self.history.pop(0)

    def get_context(self):
        if not self.history:
            return ""
        context = ""
        for u, a in self.history:
            context += f"User: {u}\nJarvis: {a}\n"
        return context
