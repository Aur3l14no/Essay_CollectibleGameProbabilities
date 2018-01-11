import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

def calc_transition(n, m):
    transition = np.zeros(shape=(m+1, m+1))
    for i in range(m):
        transition[i, i] = 1-(m-i)/n
        transition[i, i+1] = (m-i)/n
    transition[m, m] = 1
    return transition

def calc_probability(state):
    ret = 0    
    for m, probability in enumerate(state):
        if m < 12:
            continue
        if m > 18:
            break
        t = 0
        if m >= 12:
            t += 4*comb(6, 18-m)
        if m >= 11:
            t -= 2*comb(7, 18-m)
        if m >= 17:
            t -= 2*comb(1, 18-m)
        if m >= 18:
            t += 1
        ret += probability * t / comb(18, m)
    return ret


def myplot(ys):
    plt.plot(range(len(ys)), ys)
    current_milestone = 0.5
    milestone = []
    for i, v in enumerate(ys):
        if ys[i] > current_milestone:
            milestone.append((i, ys[i]))
            current_milestone += 0.1
    for stone in milestone:
        plt.annotate('({0}, {1:.1})'.format(round(stone[0]), stone[1]), xy=stone, xycoords='data',
            xytext=(-80, +10), textcoords='offset points', fontsize=16)
        plt.scatter([stone[0],],[stone[1],], 50, color ='r')
    plt.yticks(np.arange(0.0, 1.1, 0.1))
    plt.show()


def main():
    N = 104
    M = 18
    K = 500
    state = np.zeros(shape=(M+1, ))
    state[0] = 1
    transition = calc_transition(N, M)
    probabilities = []
    for i in range(K):
        probabilities.append(calc_probability(state))
        state = state.dot(transition)
        # if i % 50 == 0:
        #     print(state)
    # print(probabilities)
    myplot(probabilities)
    

if __name__ == "__main__":
    main()
