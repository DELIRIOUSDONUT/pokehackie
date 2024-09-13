    async def finals(self, players, round = 0):
        if len(players) == 1:
            return players[0]
    
        winners = []

        print(f"Round {round + 1}")
        
        # Simulate matches for each pair of players
        for i in range(0, len(players), 2):
            player1 = players[i]
            player2 = players[i + 1]
            winner = await self.play(player1, player2)
            winners.append(winner)
        
        # Recursively call tournament for the winners
        return await self.finals(winners, round + 1)