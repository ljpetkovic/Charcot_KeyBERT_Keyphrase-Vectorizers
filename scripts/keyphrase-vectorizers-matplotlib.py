# Creating the visualization for a Beamer slide without the title

fig, ax = plt.subplots(figsize=(16, 12))  # Beamer slide size with a 4:3 aspect ratio

# Adjusting the font size for better readability on a Beamer presentation
font_size_terms = 14
font_size_labels = 16

# Increase the spacing between lines for better legibility
spacing = 2
y_positions = [i * spacing for i in range(len(duplicates))]

# Plotting the terms with larger letters for improved readability
for i, term in enumerate(duplicates):
    ax.plot([0, 1], [y_positions[i], y_positions[i]], marker='o', linestyle='-', color='blue')
    ax.text(-0.1, y_positions[i], term, ha='right', va='center', fontsize=font_size_terms)
    ax.text(1.1, y_positions[i], term, ha='left', va='center', fontsize=font_size_terms)

ax.set_xlim(-0.5, 1.5)
ax.set_ylim(-1, y_positions[-1] + 1)  # Adjust the ylim based on the new spacing
ax.axis('off')  # Hide the axis

# Adding labels for "Autres" and "Charcot"
ax.text(0, y_positions[-1] + 3, 'Autres', ha='center', va='bottom', fontsize=font_size_labels, fontweight='bold')
ax.text(1, y_positions[-1] + 3, 'Charcot', ha='center', va='bottom', fontsize=font_size_labels, fontweight='bold')

# Removing the title
plt.gca().invert_yaxis()  # Invert y-axis for better layout

# Saving the image for Beamer without the title
image_path_breamer_no_title = "/mnt/data/visualisation_termes_dupliques_breamer_no_title.png"
plt.savefig(image_path_breamer_no_title, dpi=300, bbox_inches='tight')

image_path_breamer_no_title
