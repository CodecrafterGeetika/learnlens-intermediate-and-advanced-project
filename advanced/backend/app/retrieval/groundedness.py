class GroundednessChecker:

    def __init__(self, threshold: float = 0.0):
        self.threshold = threshold

    def check(self, results: list[dict]) -> bool:

      if not results:
        print("GROUNDEDNESS: No results")
        return False

      best_score = max(
        result["rerank_score"]
        for result in results
      )

      print("GROUNDEDNESS BEST SCORE:", best_score)
      print("GROUNDEDNESS THRESHOLD:", self.threshold)

      return best_score >= self.threshold