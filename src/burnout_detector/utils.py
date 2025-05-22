from typing import List


class Utils:
    @staticmethod
    def batchify(items: List, batch_size: int) -> List[List]:
        """
        Batchify a list of items.
        """
        return [items[i:i+batch_size] for i in range(0, len(items), batch_size)]