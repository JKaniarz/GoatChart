import random

num_players = 1 # how many sets of player cards to add
num_draws = 10 # how wide is the table
num_stars = 10 # how tall is the table

# Table of the card types and quantities.
# Note your advanced skills and curses in the "Added" column.
# The Base column is the 35 Basic skill cards.
# The player column is multiplied by the num_players
cards = [
    #Symbol		Added	Base	Player
    ["💀",	    1,	    4,	    0],
    ["7",		0,		0,		0],
    ["77",		0,		0,		0],
    ["{",		0,		4,		1],
    ["{7",		0,		2,		0],
    ["}",		0,		4,		0],
    ["}7",		0,		1,		1],
    ["}{",		0,		0,		1],
    ["}{7",		0,		0,		0],
    ["★",		0,		7,		0],
    ["★7",		0,		0,		0],
    ["★{",		0,		5,		1],
    ["★{7",		0,		1,		0],
    ["}★",		0,		8,		1],
    ["}★7",		0,		0,		0],
    ["}★{",		0,		0,		0],
    ["}★{7",	0,		0,		0],
    ["★★",		0,		2,		0],
    ["★★★",		0,		1,		0]]

# Return a list of cards.
# Each card is in the format:
#(skulls, stars, sevens, right halves, left halves, two halves)
# Cards with two halves have 0 additional left and right halves
def build_deck():
    deck = []
    for c in cards:
        l = c[0].count("{")
        r = c[0].count("}")
        lr = min(l,r) #count the pairs
        l -= lr #subtract out pairs
        r -= lr #subtract out pairs
        skulls = c[0].count("💀")
        stars = c[0].count("★")
        sevens = c[0].count("7")
        card = (skulls,stars,sevens,r,l,lr)
        # add coppies of the card to the deck
        for _ in range(c[1] + c[2] + num_players * c[3]):
            deck.append(card)
    return deck

# Returns the number of stars that can be made from the combination of
# symbols on the "card" which is actually the sum of all the cards in
# the draw.
def star_count(card):
    count = card[1] # whole stars
    if card[5] > 0:
        count += card[5] - 1 # make one long chain of two-half cards
        if card[3]: # try to cap one end of the chain
            count += 1
        if card[4]: # try to cap the other end of the chain
            count += 1      
        # pair up remaining half stars
        count += min(max(card[3] - 1,0),max(card[4] - 1,0)) 
    else:
        count += min(card[3],card[4]) #pair up half stars
    return count


def main():
    random.seed()
    
    deck = build_deck()

    #calculate deck stats
    card_sum = (0,0,0,0,0,0)
    non_curse_count = 0
    for card in deck:
        card_sum = tuple(map(sum, zip(card_sum, card)))
        if not card[0]:
            non_curse_count += 1

    print(str(non_curse_count)+" of " + str(len(deck)) + " cards in the deck are not curses.")
    print("On average " + "{:.2f}".format((card_sum[1] + card_sum[3] / 2 + card_sum[4] / 2 + card_sum[5]) / len(deck)) + "★ per card")
    print("On average " + "{:.2f}".format((card_sum[1] + card_sum[3] / 2 + card_sum[4] / 2 + card_sum[5]) / non_curse_count) + "★ per non-curse card")
    print()

    # build the goat chart
    goat_chart = [[0 for x in range(num_draws)] for y in range(num_stars)]
    seven_chart = [0 for x in range(num_draws)]
    num_trials = len(deck) * 1000

    for _ in range(num_trials):
        card_sum = (0,0,0,0,0,0)
        draw = random.sample(deck,num_draws)
        for i in range(num_draws):
            card_sum = tuple(map(sum, zip(card_sum, draw[i])))
            
            # add a success for each cell 1 through star_count.
            for s in range(min(star_count(card_sum),num_stars)):
                goat_chart[s][i]+=1
            seven_chart[i]+=card_sum[3]

    # print the table
    print("Draw:\t","\t".join(map(lambda x: str(x + 1),range(num_draws))))
    for i,row in enumerate(goat_chart):
        print(str(i + 1) + "★\t","\t".join(map(lambda x: "{:.0%}".format(x / num_trials), row)))

    print("7's\t","\t".join(map(lambda x: "{:.1f}".format((x / num_trials)), seven_chart)))
    
main()
