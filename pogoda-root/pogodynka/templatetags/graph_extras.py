from django import template

register = template.Library()


@register.inclusion_tag('graphs/standard.html')
def graph_for_data(prediction_stamp_location_list, colors):
    colors = ["red", "blue"]
    prediction_stamp = prediction_stamp_location_list[0]
    # {
    #     "creation_time": ...,
    #     "num_of_location": 2,
    #     "predictions_list": [ [pred, pred],
    #                           [pred, pred] ],
    #     "prediction_type": temperatureType,
    #     "prediction_name": 'temperatura,
    #     "location_list": [ 'meteo',
    #                        'politechnika'],
    #     "start_stamp": data,
    #     "end_stamp": data,
    #     "colors": ['red',
    #                'blue'],
    # }
    d = {
        "creation_time": prediction_stamp.start_stamp,
        "num_of_location": range(len([stamp.location.name for stamp in prediction_stamp_location_list])),
        "predictions_list": [stamp.predictions for stamp in prediction_stamp_location_list],
        "prediction_type": prediction_stamp.prediction_type,
        "prediction_name": prediction_stamp.prediction_type.name,
        "location_list": [stamp.location.name for stamp in prediction_stamp_location_list],
        "start_stamp": prediction_stamp.start_stamp,
        "end_stamp": prediction_stamp.start_stamp,
        "colors": colors,
    }
    d["location_and_predictions"] = zip(d['location_list'], d['predictions_list'], d['colors'])
    return d


@register.inclusion_tag('graphs/standard_future.html')
def graph_for_future(*args, **kwargs):
    return graph_for_data(*args, **kwargs)
