from django.db import migrations


def insert_data(apps, schema_editor):
    Metric = apps.get_model('base', 'Metric')

    tf = Metric(name='TF')
    tf.save()
    posf = Metric(name='POS_F')
    posf.save()
    posl = Metric(name='POS_L')
    posl.save()
    posb = Metric(name='POS_B')
    posb.save()
    cov = Metric(name='COV')
    cov.save()
    key = Metric(name='KEY')
    key.save()
    luhn = Metric(name='LUHN')
    luhn.save()
    lench = Metric(name='LEN_CH')
    lench.save()
    lenw = Metric(name='LEN_W')
    lenw.save()
    tfisf = Metric(name='TF_ISF')
    tfisf.save()
    svd = Metric(name='SVD')
    svd.save()
    titleo = Metric(name='TITLE_O')
    titleo.save()
    titlej = Metric(name='TITLE_J')
    titlej.save()
    titlec = Metric(name='TITLE_C')
    titlec.save()
    textrank = Metric(name='TEXT_RANK')
    textrank.save()


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0010_metric_remove_documentcollection_weights_and_more'),
    ]

    operations = [
        migrations.RunPython(insert_data),
    ]
