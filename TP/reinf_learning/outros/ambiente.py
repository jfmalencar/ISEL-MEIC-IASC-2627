class Ambiente:
    @abstractmethod
    def reset(self):
        """Reinicia o ambiente e retorna o estado inicial."""
        pass

    @abstractmethod
    def step(self, accao):
        """
        Executa a ação no ambiente.
        Retorna uma tupla (next_state, reward, done), onde:
        - next_state: o próximo estado após a ação
        - reward: a recompensa obtida
        - done: booleano indicando se o episódio terminou
        """
        pass
