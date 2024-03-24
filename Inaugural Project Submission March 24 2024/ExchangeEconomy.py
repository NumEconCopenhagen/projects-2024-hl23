from types import SimpleNamespace
import matplotlib.pyplot as plt
import numpy as np  # Optimize

plt.rc('text', usetex=True)  # Enable LaTeX rendering
plt.rc('font', family='serif')

class ExchangeEconomyClass:

    def __init__(self):
        
        par = self.par = SimpleNamespace()

        # a. Preferences
        par.alpha = 1/3
        par.beta = 2/3

        # b. Endowments
        par.w1A = 0.8
        par.w2A = 0.3
        # Assuming the total endowment of both goods equals 1 for each agent
        par.w1B = 1 - par.w1A
        par.w2B = 1 - par.w2A

    # Utility functions
    def utility_A(self, x1A, x2A):
        return x1A**self.par.alpha * x2A**(1-self.par.alpha)

    def utility_B(self, x1B, x2B):
        return x1B**self.par.alpha * x2B**(1-self.par.alpha)
        
    # Demand functions
    def demand_A(self, p1, p2=1.0):
        total_budget = p1*self.par.w1A + p2*self.par.w2A
        return self.par.alpha * total_budget / p1, (1 - self.par.alpha) * total_budget / p2

    def demand_B(self, p1, p2=1.0):
        total_budget = p1*self.par.w1B + p2*self.par.w2B
        return self.par.beta * total_budget / p1, (1 - self.par.beta) * total_budget / p2

    def check_market_clearing(self, p1, p2=1.0):
        x1A, x2A = self.demand_A(p1, p2)
        x1B, x2B = self.demand_B(p1, p2)

        eps1 = x1A - self.par.w1A + x1B - self.par.w1B
        eps2 = x2A - self.par.w2A + x2B - self.par.w2B

        return eps1, eps2

    # Compute errors over prices
    def compute_errors_over_prices(self):
        N = 75
        p1_range = np.linspace(0.5, 2.5, N+1)
        errors = []

        for p1 in p1_range:
            eps1, eps2 = self.check_market_clearing(p1)
            errors.append((p1, eps1, eps2))

        return errors
   

    # Illustrate the set
    def illustrate_set(self):
        par = self.par
        N = 75
        x1A_grid = np.linspace(0, 1, N+1)
        x2A_grid = np.linspace(0, 1, N+1)

        x1A_list = []
        x2A_list = []

        for x1A in x1A_grid:
            for x2A in x2A_grid:
                x1B = 1 - x1A
                x2B = 1 - x2A
                if (self.utility_A(x1A, x2A) >= self.utility_A(par.w1A, par.w2A) and
                    self.utility_B(x1B, x2B) >= self.utility_B(1-par.w1A, 1-par.w2A)):
                    x1A_list.append(x1A)
                    x2A_list.append(x2A)

        fig = plt.figure(figsize=(6, 6), dpi=150)
        ax_A = fig.add_subplot(1, 1, 1)

        ax_A.set_xlabel(r'$x_1^{A}$', fontsize=12)
        ax_A.set_ylabel(r'$x_2^{A}$', fontsize=12)

        temp = ax_A.twinx()
        temp.set_ylabel(r'$x_2^{B}$', fontsize=12)
        ax_B = temp.twiny()
        ax_B.set_xlabel(r'$x_1^{B}$', fontsize=12)
        ax_B.invert_xaxis()
        ax_B.invert_yaxis()

        ax_A.scatter(par.w1A, par.w2A, marker='s', s=50, color='black', label='Endowment')
        ax_A.scatter(x1A_list, x2A_list, marker='o', color='blue', alpha=0.6, label=r'Set $\mathcal{C}$', edgecolors='w', linewidth=0.5)

        # Add grid lines and legend
        ax_A.plot([0, 1], [0, 0], 'k-', lw=1)
        ax_A.plot([0, 1], [1, 1], 'k-', lw=1)
        ax_A.plot([0, 0], [0, 1], 'k-', lw=1)
        ax_A.plot([1, 1], [0, 1], 'k-', lw=1)
        ax_A.scatter(0.53, 0.53, marker='o', s=50, color='green', label='Max U Point')

        ax_A.set_xlim([-0.1, 1.1])
        ax_A.set_ylim([-0.1, 1.1])
        ax_B.set_xlim([1.1, -0.1])
        ax_B.set_ylim([1.1, -0.1])

        # Show plot
        ax_A.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax_A.legend(frameon=True, loc='upper right', bbox_to_anchor=(1.5, 1.0), fontsize=10)
        plt.show()

    def sum_squared_errors(p1, p1_values, eps1_values, eps2_values):
        # Calculate the sum of squared errors for a given price and corresponding errors
        idx = np.argmin(np.abs(np.array(p1_values) - p1))
        
        eps1 = eps1_values[idx]
        eps2 = eps2_values[idx]
        
        sse = eps1**2 + eps2**2  # Sum of squared errors
        
        return sse

    def find_optimal_p1(self, p1_values):
        # Define a function to minimize (negative utility)
        def neg_utility(p1):
            x1B, x2B = self.demand_B(p1)
            # Assuming goods are normalized so total amounts of good 1 and 2 are 1
            x1A, x2A = 1 - x1B, 1 - x2B
            return -self.utility_A(x1A, x2A)  # Returning negative utility for minimization

        # Convert list to numpy array and ensure it's 1D
        p1_values_np = np.asarray(p1_values).flatten()

        # Optimize (minimize) by evaluating all values in `p1_values`
        res = brute(neg_utility, ranges=[(min(p1_values_np), max(p1_values_np))], Ns=len(p1_values_np), full_output=True, finish=None)
        
        optimal_p1, max_utility_neg = res[0], -res[1]  # extract optimal price and convert utility back
        return optimal_p1, max_utility_neg
    
    def illustrate_set_2(self, point1, point2, point3):
        par = self.par
        x1A_list = []
        x2A_list = []

        # Append the three specific points
        x1A_list.append(point1[0])
        x2A_list.append(point1[1])
        x1A_list.append(point2[0])
        x2A_list.append(point2[1])
        x1A_list.append(point3[0])
        x2A_list.append(point3[1])

        fig = plt.figure(figsize=(6, 6), dpi=150)
        ax_A = fig.add_subplot(1, 1, 1)

        ax_A.set_xlabel(r'$x_1^{A}$', fontsize=12)
        ax_A.set_ylabel(r'$x_2^{A}$', fontsize=12)

        temp = ax_A.twinx()
        temp.set_ylabel(r'$x_2^{B}$', fontsize=12)
        ax_B = temp.twiny()
        ax_B.set_xlabel(r'$x_1^{B}$', fontsize=12)
        ax_B.invert_xaxis()
        ax_B.invert_yaxis()

        # Scatter plot for three specific points
        ax_A.scatter(x1A_list[0], x2A_list[0], marker='o', color='blue', alpha=0.6, label='From 3)', edgecolors='w', linewidth=0.5)
        ax_A.scatter(x1A_list[1], x2A_list[1], marker='o', color='red', alpha=0.6, label='From 4)', edgecolors='w', linewidth=0.5)
        ax_A.scatter(x1A_list[2], x2A_list[2], marker='o', color='green', alpha=0.6, label='From 5)', edgecolors='w', linewidth=0.5)

        # Additional Plot details
        ax_A.plot([0, 1], [0, 1], 'k--', lw=1, label='Pareto Efficient Path for the Social Planner')
        ax_A.plot([0, 1], [0, 0], 'k-', lw=1)
        ax_A.plot([0, 1], [1, 1], 'k-', lw=1)
        ax_A.plot([0, 0], [0, 1], 'k-', lw=1)
        ax_A.plot([1, 1], [0, 1], 'k-', lw=1)
        ax_A.set_xlim([-0.1, 1.1])
        ax_A.set_ylim([-0.1, 1.1])
        ax_B.set_xlim([1.1, -0.1])
        ax_B.set_ylim([1.1, -0.1])

        # Additional plot details
        ax_A.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax_A.legend(frameon=True, loc='upper right', bbox_to_anchor=(2, 1.0), fontsize=10)

        plt.show() 