"""Utility functions for averages and related metrics."""
import statistics


def calculate_average(marks):
    """Return the arithmetic mean of an iterable of numeric marks.

    Args:
        marks (iterable): numbers representing marks/scores.

    Returns:
        float: mean of the marks.
    """
    return statistics.mean(marks)
