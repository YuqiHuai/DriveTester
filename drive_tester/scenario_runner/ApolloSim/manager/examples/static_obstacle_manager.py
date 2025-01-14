import copy

from loguru import logger
from typing import List

from apollo_sim.registry import ACTOR_REGISTRY
from apollo_sim.agents.static_obstacle import StaticObstacleConfig, StaticObstacleAgent
from apollo_sim.sim_env import SimEnv

from drive_tester.scenario_runner.ApolloSim.manager import SubScenarioManager


class StaticObstacleManager(SubScenarioManager):

    def __init__(
            self,
            scenario_idx: str,
            config_pool: List[StaticObstacleConfig],
            sim_env: SimEnv,
            output_folder: str,
            # other configs
            debug: bool = False,
    ):

        super(StaticObstacleManager, self).__init__(
            scenario_idx=scenario_idx,
            config_pool=config_pool,
            sim_env=sim_env,
            output_folder=output_folder,
            debug=debug
        )

    def _initialize(self):
        for i, config in enumerate(self.config_pool):
            actor_class = ACTOR_REGISTRY.get(config.category)
            actor_location = copy.deepcopy(config.location)
            actor = actor_class(
                id=config.idx,
                location=actor_location,
                role=config.role
            )
            self.sim_env.register_actor(actor)

            self.agent_list.append(
                StaticObstacleAgent(
                    actor=actor,
                    config=config,
                    sim_env=self.sim_env,
                    debug=self.debug,
                    output_folder=self.output_folder,
                    scenario_idx=self.scenario_idx
                )
            )