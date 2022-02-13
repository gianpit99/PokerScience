import datetime as dt

class Player:
    def __init__(self, playerName):
        self.playerName = playerName
        self.id = hash(str(dt.datetime.now()))

        self.hand = None
        self.payroll = None

        self.numHandsPlayed = 0
        self.numHandsExperianced = 0
        self.numHandsWon = 0
        self.numHandsLost = 0

    def action(pos, pot, bfrplyrs, afrplyrs, table):
        '''
        ~ in texas hold'm, there are a max of 23 players
            52 - 5 = 47, 47/2 = 23.5

        - incorporate re-raising?

        parameters
        ----------
        pot : pot size

        pos : position relative to dealer

        bfrplyrs : players that played before
        afrplyrs : players that played after
            information used:
                - there play style class (prediction on what type of player they are based on play history, latent space?)
                - there payroll
                - there bet size (if applicable)
                - there type of bet (check, raise, fold)
                - Weather they're (in the pot, out of the pot, havent acted, not a player)
        - total number of players before
        - total number of players after
        - active number of players before
        - active number of players after

        table : table cards

        parameters in class
        -------------------
        self.hand -> hand strength encoding
        self.payroll ->

        returns
        -------

        action : bet, check, raise

        bet amount :


        '''
