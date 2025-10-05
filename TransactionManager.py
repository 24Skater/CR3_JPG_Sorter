import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from Logger import logger

class Transaction:
    """Represents a single file move transaction."""
    
    def __init__(self, source: str, destination: str, timestamp: str = None):
        self.source = source
        self.destination = destination
        self.timestamp = timestamp or datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            "source": self.source,
            "destination": self.destination,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Transaction':
        return cls(data["source"], data["destination"], data.get("timestamp"))

class TransactionManager:
    """Manages file move transactions for undo/rollback functionality."""
    
    def __init__(self, transaction_file: str = "last_transaction.json"):
        self.transaction_file = transaction_file
        self.current_transactions: List[Transaction] = []
    
    def start_batch(self) -> None:
        """Start a new batch of transactions."""
        self.current_transactions = []
        logger.info("Started new transaction batch")
    
    def add_transaction(self, source: str, destination: str) -> None:
        """Add a file move to the current transaction batch."""
        transaction = Transaction(source, destination)
        self.current_transactions.append(transaction)
        logger.debug(f"Transaction recorded: {source} -> {destination}")
    
    def commit_batch(self) -> None:
        """Save the current batch of transactions to file."""
        if not self.current_transactions:
            logger.warning("No transactions to commit")
            return
        
        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "count": len(self.current_transactions),
                "transactions": [t.to_dict() for t in self.current_transactions]
            }
            
            with open(self.transaction_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Committed {len(self.current_transactions)} transactions to {self.transaction_file}")
        except Exception as e:
            logger.error(f"Failed to commit transactions: {e}")
    
    def can_undo(self) -> bool:
        """Check if there are transactions available to undo."""
        return os.path.exists(self.transaction_file)
    
    def get_last_transaction_info(self) -> Optional[Dict]:
        """Get information about the last transaction batch."""
        if not self.can_undo():
            return None
        
        try:
            with open(self.transaction_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return {
                "timestamp": data.get("timestamp"),
                "count": data.get("count", 0)
            }
        except Exception as e:
            logger.error(f"Failed to read transaction info: {e}")
            return None
    
    def undo_last_batch(self) -> tuple[int, int, List[str]]:
        """
        Undo the last batch of transactions.
        
        Returns:
            Tuple of (successful_count, failed_count, errors)
        """
        if not self.can_undo():
            logger.warning("No transactions to undo")
            return 0, 0, ["No transactions to undo"]
        
        try:
            with open(self.transaction_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            transactions = [Transaction.from_dict(t) for t in data.get("transactions", [])]
            logger.info(f"Starting undo of {len(transactions)} transactions")
            
            successful = 0
            failed = 0
            errors = []
            
            # Undo in reverse order
            for transaction in reversed(transactions):
                try:
                    # Check if destination file still exists
                    if not os.path.exists(transaction.destination):
                        logger.warning(f"Destination file no longer exists: {transaction.destination}")
                        failed += 1
                        errors.append(f"File not found: {os.path.basename(transaction.destination)}")
                        continue
                    
                    # Check if source location is available
                    if os.path.exists(transaction.source):
                        logger.warning(f"Source location already has a file: {transaction.source}")
                        failed += 1
                        errors.append(f"Cannot restore, file exists: {os.path.basename(transaction.source)}")
                        continue
                    
                    # Create source directory if needed
                    os.makedirs(os.path.dirname(transaction.source), exist_ok=True)
                    
                    # Move file back
                    import shutil
                    shutil.move(transaction.destination, transaction.source)
                    successful += 1
                    logger.debug(f"Undone: {transaction.destination} -> {transaction.source}")
                    
                except Exception as e:
                    failed += 1
                    error_msg = f"{os.path.basename(transaction.destination)}: {str(e)}"
                    errors.append(error_msg)
                    logger.error(f"Failed to undo transaction: {e}")
            
            # Remove transaction file after successful undo
            if successful > 0:
                try:
                    os.remove(self.transaction_file)
                    logger.info(f"Undo complete. Success: {successful}, Failed: {failed}")
                except Exception as e:
                    logger.warning(f"Could not remove transaction file: {e}")
            
            return successful, failed, errors
            
        except Exception as e:
            logger.error(f"Failed to undo transactions: {e}")
            return 0, 0, [f"Undo failed: {str(e)}"]

# Global instance
transaction_manager = TransactionManager()

