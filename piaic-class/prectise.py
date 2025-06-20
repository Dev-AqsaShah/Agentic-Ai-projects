from agents import Runner, RunHooks, RunContextWrapper, Agent
from typing import TypeVar


class MyCustomRunHooks(RunHooks):
    def on_start(self, context: RunContextWrapper, agent: Agent):
        print(f"Starting run for agent: {agent.name}")
        
    def on_end(self, agent, output):
        print(f"Run completed for agent: {agent.name}, output: {output.final_output}")
        

T = TypeVar("T")


obj = {
    
}