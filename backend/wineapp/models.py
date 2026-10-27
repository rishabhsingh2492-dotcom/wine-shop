from django.db import models

FEATURES = ['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar', 'chlorides',
            'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density', 'ph', 'sulphates', 'alcohol']
COLS = FEATURES + ['quality']


class WineSample(models.Model):
    """One row of the UCI red wine quality dataset."""
    fixed_acidity = models.FloatField()
    volatile_acidity = models.FloatField()
    citric_acid = models.FloatField()
    residual_sugar = models.FloatField()
    chlorides = models.FloatField()
    free_sulfur_dioxide = models.FloatField()
    total_sulfur_dioxide = models.FloatField()
    density = models.FloatField()
    ph = models.FloatField()
    sulphates = models.FloatField()
    alcohol = models.FloatField(db_index=True)
    quality = models.IntegerField(db_index=True)


class PredictionRecord(models.Model):
    features = models.JSONField()
    predicted_raw = models.FloatField()
    predicted_score = models.IntegerField()  # raw value rounded and clipped to 0..10
    model_name = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
