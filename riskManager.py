

import random, math
TOTAL_CAPITAL_STARTER = 100

def growthSimulator(startTC, growthRate, trades):
    resultTC = startTC
    for i in range(trades):
        resultTC = resultTC * growthRate
    print(f"using growthSimulator, start with {startTC}, after {trades} trades, result TC: {resultTC}")
    return resultTC

def strategyEvaluation(params = {}):
    totalCapital = params.get('totalCapitalStarter', TOTAL_CAPITAL_STARTER)
    strategyReward = params.get('strategyReward', 0.05) 
    strategyWinPercentage = params.get('strategyWinPercentage', 0.7)
    strategyFailPenaulty = params.get('strategyFailPenaulty', 0.05)
    print(f"Evaluating strategy with totalCapital: {totalCapital}, strategyReward: {strategyReward}, strategyWinPercentage: {strategyWinPercentage}, strategyFailPenaulty: {strategyFailPenaulty}")
    print(f"risk/reward ratio: {strategyWinPercentage * strategyReward / ((1 - strategyWinPercentage) * strategyFailPenaulty)}")

    for i in range(100):
        # simulate a win
        if (random.randint(1, 100) / 100) <= strategyWinPercentage:
            totalCapital = totalCapital * (1 + strategyReward)
        else:
            totalCapital = totalCapital * (1 - strategyFailPenaulty)
    print(f"After 100 trades in simulation, the total capital is {totalCapital / TOTAL_CAPITAL_STARTER} times original value.")

    tc_expo_growth_ratio = 1 + strategyReward * strategyWinPercentage - strategyFailPenaulty * (1 - strategyWinPercentage)
    print(f"tc_expo_growth_ratio: {tc_expo_growth_ratio}")
    if tc_expo_growth_ratio < 1: 
        print(f"strategy won't work. tc_expo_growth_ratio < 1. tc_expo_growth_ratio: {tc_expo_growth_ratio}")
        print("End of evaluation. \n\n")
        return
    trades_to_reach_double_TC = int(math.log(2, tc_expo_growth_ratio)) + 1
    estimated_TC = math.pow(tc_expo_growth_ratio, trades_to_reach_double_TC) * TOTAL_CAPITAL_STARTER
    print(f"Trades to reach double TC is {trades_to_reach_double_TC}. After this amount of trades, estimated TC is: {estimated_TC}")
    print("End of evaluation. \n\n")

# evaluation of a winning strategy
strategyEvaluation({
    'totalCapitalStarter': 200,
    'strategyReward': 0.05,
    'strategyWinPercentage': 0.7,
    'strategyFailPenaulty': 0.05
})

# evaluation of a leverage strategy
strategyEvaluation({
    'totalCapitalStarter': 200,
    'strategyReward': 0.05 * 20,
    'strategyWinPercentage': 0.7,
    'strategyFailPenaulty': 1.0
})

# evaluation of a leverage strategy
strategyEvaluation({
    'totalCapitalStarter': 200,
    'strategyReward': 0.05 * 50,
    'strategyWinPercentage': 0.3,
    'strategyFailPenaulty': 1.0
})

# evaluation of a leverage strategy
strategyEvaluation({
    'totalCapitalStarter': 200,
    'strategyReward': 0.05 * 4,
    'strategyWinPercentage': 0.7,
    'strategyFailPenaulty': 0.2
})