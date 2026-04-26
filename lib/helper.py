import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path

#---------------------------------------------------------------------------------------
# Generic plotting utility
#---------------------------------------------------------------------------------------

class Helper:
    def plot_solution(self, funcs=None, a=None, b=None, solutions=None, 
                      labels=None, title="Function Plot", save_path=None, 
                      xvals=None, show_zero_line=True, figsize=(8, 6),
                      colors=None, linestyles=None, markers=None):
        """
        Ultra-generic universal plotter for ANY function/data type from the Tools class.
        
        Parameters
        ----------
        funcs : callable, list of callables, tuple (xvals, yvals), list of tuples, or None
            - Single callable: plots y = f(x) over [a, b]
            - List of callables: plots multiple functions on same axes
            - Tuple (x, y) arrays: plots raw data points (e.g., ODE solutions, interpolation nodes)
            - List of tuples: plots multiple datasets
            - None: requires xvals and yvals via solutions parameter
        
        a, b : float, optional
            Domain bounds for univariate functions. If None, auto-scales from xvals or funcs.
        
        solutions : array-like, dict, or None
            - Array-like: x-coordinates of points to mark as red scatter plots
            - Dict with 'x' and 'y': explicit marking points {x, y, label_list}
            - None: no solution markers
        
        labels : str or list of str, optional
            Single label or list of labels for the plotted functions/datasets.
        
        title : str
            Plot title.
        
        save_path : str or Path, optional
            Path to save figure. If None and backend is non-interactive, defaults to plots/plot_*.png
        
        xvals : array-like, optional
            Explicit x-values for evaluating functions. If None, auto-generated from [a, b].
        
        show_zero_line : bool
            Whether to draw a horizontal line at y=0.
        
        figsize : tuple
            Figure size (width, height).
        
        colors, linestyles, markers : str or list, optional
            Line/marker styling per function. Defaults provided automatically.
        
        Examples
        --------
        # Plot single root-finding function
        plot_solution(f, a=0, b=5, solutions=[2.3], title="Root at x=2.3")
        
        # Plot multiple interpolators
        P1, a1, x1 = tool.newton_interpolator(x_data, y_data)
        P2, a2, x2 = tool.lagrange_interpolator(x_data, y_data)
        plot_solution([P1, P2], a=x_data.min(), b=x_data.max(), 
                      labels=["Newton", "Lagrange"])
        
        # Plot LSOE Solution and Residual
        sol, err = tool.solve_lsoe(A, B) A = Array 1, B = Array 2
        -Solution
        plot_solution([(np.arange(1, len(sol)+1), sol)], 
                            labels="LSOE Solution", title="LSOE Solution Vector")
        
        -Residual
        A = np.asarray(Array1, dtype=float)
        B = np.asarray(Array2, dtype=float)
        residual = A @ sol - B
        plot_solution(funcs=(np.arange(1, len(sol)+1), residual),
                            labels="Residual (A@x - B)",title="Unit04 LSOE Residual")

        # Plot ODE solution trajectory
        t, y = tool.runge_kutta(f, x0=0, xn=2, h=0.01, y0=1)
        plot_solution((t, y), labels="RK4 Solution", title="ODE Trajectory")
        
        # Plot interpolation nodes
        plot_solution((x_nodes, y_nodes), labels="Data Points", markers='o')
        """
        # Normalize funcs into a list
        if funcs is None:
            func_list = []
            data_list = []
        elif isinstance(funcs, tuple) and len(funcs) == 2 and \
             isinstance(funcs[0], (list, np.ndarray)) and isinstance(funcs[1], (list, np.ndarray)):
            # Single tuple of (x, y) arrays
            func_list = []
            data_list = [funcs]
        elif isinstance(funcs, list):
            func_list = []
            data_list = []
            for item in funcs:
                if isinstance(item, tuple) and len(item) == 2:
                    data_list.append(item)
                elif callable(item):
                    func_list.append(item)
                else:
                    raise TypeError(f"List must contain callables or (x,y) tuples; got {type(item)}")
        elif callable(funcs):
            func_list = [funcs]
            data_list = []
        else:
            raise TypeError(f"funcs must be callable, tuple (x,y), or list thereof; got {type(funcs)}")
        
        # Normalize labels
        total_items = len(func_list) + len(data_list)
        if isinstance(labels, str):
            label_list = [labels]
        elif labels is None:
            label_list = [f"Dataset {i+1}" for i in range(total_items)]
        elif isinstance(labels, (list, tuple)):
            label_list = list(labels)
        else:
            label_list = [str(labels)]
        
        # Pad labels to match number of functions/datasets
        while len(label_list) < total_items:
            label_list.append(f"Dataset {len(label_list)+1}")
        
        # Determine x-values for function evaluation
        if xvals is None:
            if a is not None and b is not None:
                if a > b:
                    a, b = b, a
                xvals = np.linspace(float(a), float(b), 400)
            else:
                # Try to infer from data_list
                if data_list:
                    all_x = np.concatenate([np.asarray(d[0], dtype=float).flatten() for d in data_list])
                    a = all_x.min() if a is None else a
                    b = all_x.max() if b is None else b
                    xvals = np.linspace(float(a), float(b), 400)
                else:
                    raise ValueError("Must provide a, b or xvals when plotting functions.")
        
        xvals = np.asarray(xvals, dtype=float)
        
        # Setup figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Default styling
        default_colors = plt.cm.tab10(np.linspace(0, 1, max(total_items, 1)))
        default_linestyles = ['-', '--', '-.', ':'] * (total_items // 4 + 1)
        default_markers = [None, 'o', 's', '^', 'v', 'd', 'x', '+'] * (total_items // 8 + 1)
        
        if colors is None:
            colors = default_colors
        if linestyles is None:
            linestyles = default_linestyles
        if markers is None:
            markers = default_markers
        
        # Ensure they're lists
        colors = [colors] if isinstance(colors, str) else list(colors)
        linestyles = [linestyles] if isinstance(linestyles, str) else list(linestyles)
        markers = [markers] if markers is None or isinstance(markers, str) else list(markers)
        
        # Plot functions
        for idx, f in enumerate(func_list):
            try:
                yvals = f(xvals)
            except Exception:
                # Try element-wise evaluation
                yvals = np.array([f(xi) for xi in xvals], dtype=float)
            
            color = colors[idx % len(colors)]
            linestyle = linestyles[idx % len(linestyles)]
            ax.plot(xvals, yvals, label=label_list[idx], color=color, 
                   linestyle=linestyle, linewidth=2, zorder=2)
        
        # Plot datasets (x, y) pairs
        for idx, (x_data, y_data) in enumerate(data_list):
            x_data = np.asarray(x_data, dtype=float)
            y_data = np.asarray(y_data, dtype=float)
            
            func_idx = len(func_list) + idx
            color = colors[func_idx % len(colors)]
            linestyle = linestyles[func_idx % len(linestyles)]
            marker = markers[func_idx % len(markers)]
            
            # Always draw the connecting line for datasets.
            # If a marker is requested, add it on top so points are still visible.
            ax.plot(
                x_data,
                y_data,
                label=label_list[func_idx],
                color=color,
                linestyle=linestyle,
                linewidth=2,
                zorder=2,
            )

            if marker is not None:
                ax.scatter(
                    x_data,
                    y_data,
                    color=color,
                    marker=marker,
                    s=60,
                    zorder=3,
                )
        
        # Plot solution markers if provided
        if solutions is not None:
            if isinstance(solutions, dict):
                sol_x = np.asarray(solutions.get('x', []), dtype=float)
                sol_y = np.asarray(solutions.get('y', []), dtype=float)
                sol_labels = solutions.get('labels', None)
            else:
                sol_x = np.asarray(solutions, dtype=float).flatten()
                sol_labels = None
                # Evaluate functions at solution points
                if func_list:
                    sol_y = func_list[0](sol_x)
                elif data_list:
                    sol_y = np.interp(sol_x, data_list[0][0], data_list[0][1])
                else:
                    sol_y = np.zeros_like(sol_x)
            
            for i, (x_sol, y_sol) in enumerate(zip(sol_x, sol_y)):
                if sol_labels and i < len(sol_labels):
                    lbl = sol_labels[i]
                else:
                    lbl = f"x={x_sol:.4f}" if i == 0 else None
                ax.scatter([x_sol], [y_sol], c="red", s=100, marker='*', 
                          label=lbl, zorder=5, edgecolors='darkred', linewidth=1)
        
        # Styling
        if show_zero_line:
            ax.axhline(0, color="black", linewidth=0.8, alpha=0.5, zorder=1)
        
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_xlabel("x", fontsize=11)
        ax.set_ylabel("y", fontsize=11)
        ax.grid(True, alpha=0.3, zorder=0)
        ax.legend(loc='best', framealpha=0.95)
        plt.tight_layout()
        
        # Save or show
        backend = matplotlib.get_backend().lower()
        if "agg" in backend:
            if save_path is None:
                save_path = Path("plots") / f"plot_{title.replace(' ', '_').lower()}.png"
            output = Path(save_path)
            output.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output, dpi=150, bbox_inches='tight')
            print(f"Non-interactive backend '{backend}' detected; saved to {output}")
        else:
            plt.show()

        plt.close()
