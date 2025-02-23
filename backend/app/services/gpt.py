class GPTService:
    @staticmethod
    def generate_talent_portrait(text: str) -> str:
        # Mock implementation for testing
        return "具有8年Python开发经验的高级工程师，在微服务架构和分布式系统方面有丰富经验"

    @staticmethod
    def extract_job_tags(text: str) -> list:
        # Mock implementation for testing
        return ["Python", "微服务", "分布式系统", "8年经验"]

    @staticmethod
    def extract_resume_tags(text: str) -> list[dict]:
        # Mock implementation for testing
        return [{"name": "Python"}, {"name": "FastAPI"}]
