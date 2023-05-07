
import json
from typing import Callable, Dict, List, Optional, Union, Any
from functools import wraps

from flowpilot import *

class Pipeline:
    def __init__(self, flow_pilot: FlowPilot):
        self.flow_pilot = flow_pilot
        self.steps = []

    def add_step(self, category: str, func: Callable, *args, **kwargs) -> None:
        self._validate_function_category(func, category)
        self.steps.append((func, args, kwargs))

    def _validate_function_category(self, func: Callable, category: str) -> None:
        """Validate that the function belongs to the specified category."""
        if not hasattr(func, "__category__"):
            raise ValueError(f"Function '{func.__name__}' is not registered in any category.")
        if func.__category__ != category:
            raise ValueError(f"Function '{func.__name__}' does not belong to category '{category}'.")

    def execute(self) -> Any:
        data = None
        for step, step_args, step_kwargs in self.steps:
            if data is None:
                data = step(*step_args, **step_kwargs)
            else:
                data = step(data, *step_args, **step_kwargs)
        return data
    
    def show_pipeline_steps(self) -> None:
        """Display the logical flow of the functions in the pipeline."""
        if not self.steps:
            print("The pipeline is empty.")
            return

        print("Pipeline steps:")
        for i, (step, step_args, step_kwargs) in enumerate(self.steps, start=1):
            step_category = step.__category__
            step_name = step.__name__
            step_args_str = ", ".join(map(str, step_args)) if step_args else ""
            step_kwargs_str = ", ".join(f"{k}={v}" for k, v in step_kwargs.items()) if step_kwargs else ""
            step_params_str = step_args_str + (", " if step_args_str and step_kwargs_str else "") + step_kwargs_str

            print(f"{i}. [{step_category}] {step_name}({step_params_str})")
            
    def get_pipeline_steps_json(self) -> str:
        
        """Return the pipeline steps as a JSON string."""
        steps_data = [
            {"name": step.__name__, "category": step.__category__}
            for step, _, _ in self.steps
        ]
        return json.dumps(steps_data)
