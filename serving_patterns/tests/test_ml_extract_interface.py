import pytest
from app.ml import extract_interface
from typing import Tuple


filepath = 'app/ml/models/iris_svc_sklearn.yaml'


@pytest.mark.parametrize(
    ('filepath'),
    [(filepath)]
)
def test_extract_interface_yaml(filepath):
    interface = extract_interface.extract_interface_yaml(filepath)
    model_name = list(interface.keys())[0]
    assert isinstance(interface[model_name]['data_interface']['input_shape'], Tuple)
    assert isinstance(interface[model_name]['data_interface']['input_type'], str)
    assert isinstance(interface[model_name]['data_interface']['output_shape'], Tuple)
    assert isinstance(interface[model_name]['data_interface']['output_type'], str)
    assert isinstance(interface[model_name]['meta']['model_filename'], str)
    assert isinstance(interface[model_name]['meta']['prediction_type'], str)
    assert isinstance(interface[model_name]['meta']['prediction_runtime'], str)
