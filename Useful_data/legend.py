import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from math import pi

def legend():
    # Définition des couleurs
    reds = ['#FF0000', '#FF4D00', '#FF8000', '#FFB300', '#FFCC00']  # Nuances de rouge à orange
    blues = ['#0000FF', '#0066CC', '#33CC99', '#66CC66', '#99FF33']  # Nuances de bleu à vert
    legend = ["800 [Nm]", "600 [Nm]", "400 [Nm]", "200 [Nm]", "100 [Nm]"]
    
    # Création de la figure et des axes
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Définir les positions des rectangles
    rect_width = 0.4
    spacing = 0.1
    rect1_x = 0.1
    rect2_x = rect1_x + rect_width + spacing
    
    # Dessiner les rectangles et ajouter les lignes de couleurs
    for i, (red, blue) in enumerate(zip(reds, blues)):
        # Rectangle 1 (Rouge)
        ax.add_patch(patches.Rectangle((rect1_x, 1 - (i + 1) * 0.2), rect_width, 0.18, linewidth=0, facecolor=red))
    
        # Rectangle 2 (Bleu)
        ax.add_patch(patches.Rectangle((rect2_x, 1 - (i + 1) * 0.2), rect_width, 0.18, linewidth=0, facecolor=blue))
        ax.text(rect2_x + rect_width + 0.02, 1 - (i + 1) * 0.2 + 0.09, legend[i], va='center', ha='left', fontsize=14)
    
    # Ajouter des textes sous les rectangles avec une taille de police plus grande
    ax.text(rect1_x + rect_width / 2, 1.05, 'Traction', ha='center', va='center', fontsize=16)
    ax.text(rect2_x + rect_width / 2, 1.05, 'Propulsion', ha='center', va='center', fontsize=16)
    
    # Configurer les axes
    ax.set_xlim(0, 1.6)
    ax.set_ylim(0, 1)
    ax.axis('off')  # Désactiver les axes
    
    # Afficher
    plt.savefig("legend.pdf")
    plt.show()



def graph_1():
    fig, ax = plt.subplots(1)
    u = 1.  # x-position of the center
    v = 0   # y-position of the center
    a = 2.  # radius on the x-axis
    a2 = 1.7
    b = 1.5  # radius on the y-axis
    b2 = 1.2

    t = np.linspace(-2, 2, 100)
    x = np.linspace(-2, 2, 100)
    y = (1 - 1/2 * x) * 0.5
    y2 = (1 - 1/2 * x) * 0.4

    plt.plot(t, -0.15 * (t + 2) * (t - 2), color='red', linewidth=1.5)
    plt.plot(t, -0.25 * (t + 2) * (t - 2), color='blue', linewidth=2)
    plt.plot(x, y2,color ='tab:cyan')
    plt.plot(x, y, color = 'tab:orange')

    plt.ylim(0, 1.2)
    plt.axvline(x=-0.33, ymin=0, ymax=0.48, color='green', ls='--')
    plt.axvline(x=-1.19, ymin=0, ymax=0.53, color='green', ls='--')
    plt.axvline(x=0, ymin=0, ymax=1, color='black', ls='-')
    plt.grid(color='lightgray', linestyle='--')

    plt.text(-2, -0.1, "-a", fontsize=12, ha='center', color='black')
    plt.text(2, -0.1, "a", fontsize=12, ha='center', color='black')
    plt.text(0, -0.1, "0", fontsize=12, ha='center', color='black')
    plt.text(-0.33, -0.1, "x*", fontsize=12, ha='center', color='red')
    plt.text(-1.19, -0.1, "x*", fontsize=12, ha='center', color='blue')
    
    plt.text(1.1, 0.08, r"$\alpha$", fontsize=12, ha='center', color='tab:orange')
    plt.text(1.4, 0.02, r"$\alpha$", fontsize=12, ha='center', color='tab:cyan')

    plt.text(-0.2, 1.08, r"$\frac{dF_{lat}}{dx}$", fontsize=15, ha='center', color='black')
    
   
    # Parameters for the arc
    r = 0.5  # Radius of the arc
    r2 = 0.8

    # Create points for the arc
    arc_t = np.linspace(np.pi-0.2, np.pi, 100)
    arc_x = 2 + r * np.cos(arc_t)
    arc_y = r * np.sin(arc_t)

    arc_t2 = np.linspace(np.pi-0.24, np.pi, 100)
    arc_x2 = 2 + r2 * np.cos(arc_t2)
    arc_y2 = r2 * np.sin(arc_t2)
    # Plot the arc
    plt.plot(arc_x, arc_y, linestyle='-', linewidth=2, color = 'tab:cyan')
    plt.plot(arc_x2, arc_y2, linestyle='-', linewidth=2,color = 'tab:orange')
    # Hide axes
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)
    
    # Save the plot as a PDF and show the plot
    plt.savefig('graph_1.pdf')
    plt.show()

graph_1()

    
    
    
    
    