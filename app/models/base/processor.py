from abc import ABC, abstractmethod
from typing import Dict, Any, TypeVar, Generic

T = TypeVar('T')

class BaseProcessor(Generic[T], ABC):
    """Base class for all data processors.
    
    This abstract base class defines the interface that all data processors must implement.
    It uses generics to allow type-specific processing of different data types.
    
    Attributes:
        None
        
    Methods:
        process: Abstract method that must be implemented by all processors
    """
    
    @abstractmethod
    def process(self, data: T, preprocessing_options: Dict[str, bool], 
                augmentation_options: Dict[str, bool]) -> Dict[str, T]:
        """Process the input data according to the specified options.
        
        Args:
            data: The input data to process
            preprocessing_options: Dictionary of preprocessing options and their states
            augmentation_options: Dictionary of augmentation options and their states
            
        Returns:
            Dictionary containing original, preprocessed, and augmented versions of the data
        """
        pass 