import pytest
from typing import List
import numpy as np

from app.ml.abstract_predictor import BaseData, BaseDataExtension


f_data = [[0.1, 0.9, 1.1]]
i_data = [[1, 2, 3]]


@pytest.mark.parametrize(('data',
                          'np_data',
                          'input_shape',
                          'input_type',
                          'prediction',
                          'output_shape',
                          'prediction_proba'),
                         [(f_data,
                           np.array(f_data),
                           (1,
                               3),
                           'float',
                           0,
                           (1,
                               4),
                           np.array([[0.1,
                                      0.2,
                                      0.3,
                                      0.4]]))])
def test_BaseData(
        mocker,
        data,
        np_data,
        input_shape,
        input_type,
        prediction,
        output_shape,
        prediction_proba):
    class MockData(BaseData):
        testf_data: List[List[int]] = [[5.1, 3.5, 1.4, 0.2]]

    mock_data = MockData()
    mock_data.data = data
    mock_data.np_data = np_data
    mock_data.input_type = input_type
    mock_data.prediction = prediction
    mock_data.prediction_proba = prediction_proba
    mock_data.input_shape = input_shape
    mock_data.output_shape = output_shape


@pytest.mark.parametrize(
    ('data', 'np_data', 'input_shape', 'input_type', 'expected_input_datatype', 'prediction', 'output_shape', 'output_type', 'expected_output_datatype', 'prediction_proba'),
    [(f_data, np.array(f_data).astype(np.float), (1, 3), 'float', np.float, 0, (1, 4), 'float64', np.float64, np.array([[0.1, 0.2, 0.3, 0.4]])),
     (f_data, np.array(f_data).astype(np.float64), (1, 3), 'float64', np.float64, 0, (1, 4), 'float64', np.float64, np.array([[0.1, 0.2, 0.3, 0.4]])),
     (f_data[0], np.array(f_data).astype(np.float32), (1, 3), 'float32', np.float32, 0, (1, 4), 'float64', np.float64, np.array([0.1, 0.2, 0.3, 0.4])),
     (i_data, np.array(i_data).astype(np.int8), (1, 3), 'int8', np.int8, 0, (1, 4), 'float64', np.float64, np.array([[0.1, 0.2, 0.3, 0.4]])),
     (i_data[0], np.array(i_data).astype(np.int16), (1, 3), 'int16', np.int16, 0, (1, 4), 'float64', np.float64, np.array([0.1, 0.2, 0.3, 0.4]))]
)
def test_BaseDataExtension(
        mocker,
        data,
        np_data,
        input_shape,
        input_type,
        expected_input_datatype,
        prediction,
        output_shape,
        output_type,
        expected_output_datatype,
        prediction_proba):
    class MockData(BaseData):
        testf_data: List[List[int]] = [[5.1, 3.5, 1.4, 0.2]]

    mock_data = MockData()
    mock_data.data = data
    mock_data.input_shape = input_shape
    mock_data.input_type = input_type
    mock_data.prediction = prediction
    mock_data.output_shape = output_shape
    mock_data.output_type = output_type
    mock_data.prediction_proba = prediction_proba

    mock_base_data_extension = BaseDataExtension(data_object=mock_data)
    mock_base_data_extension.convert_input_data_to_np_data()
    mock_base_data_extension.convert_output_to_np()
    assert mock_data.np_data.shape == mock_data.input_shape
    assert mock_data.np_data.dtype == expected_input_datatype
    assert mock_data.prediction_proba.shape == mock_data.output_shape
    assert mock_data.prediction_proba.dtype == expected_output_datatype
    print()
    print(mock_data.data)
    print(mock_data.np_data)
    print(mock_data.np_data.shape)
    print(mock_data.np_data.dtype)
    print(mock_data.prediction_proba.shape)
    print(mock_data.prediction_proba.dtype)
    np.testing.assert_equal(mock_data.np_data, np_data)
