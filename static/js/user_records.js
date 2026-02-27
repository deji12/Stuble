const colors = [
    'linear-gradient(90deg, #667eea, #764ba2)',
    'linear-gradient(90deg, #10b981, #059669)',
    'linear-gradient(90deg, #f59e0b, #d97706)',
    'linear-gradient(90deg, #ec4899, #db2777)',
    'linear-gradient(90deg, #8b5cf6, #7c3aed)',
    'linear-gradient(90deg, #ef4444, #dc2626)'
];

const iconColors = ['#667eea', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6', '#ef4444'];

document.querySelectorAll('.record-color-bar').forEach((bar, index) => {
    bar.style.background = colors[index % colors.length];
});

document.querySelectorAll('.collection-icon i').forEach((icon, index) => {
    icon.style.color = iconColors[index % iconColors.length];
});