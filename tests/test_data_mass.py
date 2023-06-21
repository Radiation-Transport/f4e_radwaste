import unittest

import pandas as pd

from f4e_radwaste.constants import KEY_VOXEL, KEY_MATERIAL, KEY_CELL, KEY_MASS_GRAMS
from f4e_radwaste.data_formats.data_mass import DataMass


class DataMassTests(unittest.TestCase):
    def setUp(self):
        # Create a valid DataFrame for testing
        data = {
            KEY_VOXEL: [1, 1, 2, 3],
            KEY_MATERIAL: [10, 20, 10, 40],
            KEY_CELL: [11, 12, 11, 14],
            KEY_MASS_GRAMS: [2.34, 3.13, 1.09, 10.2],
        }
        df = pd.DataFrame(data)
        df.set_index([KEY_VOXEL, KEY_MATERIAL, KEY_CELL], inplace=True)

        # Initialize the validator with the DataFrame
        self.data_mass = DataMass(df)

    def test_validate_dataframe_format_valid(self):
        self.assertIsInstance(self.data_mass, DataMass)

    def test_validate_dataframe_format_invalid(self):
        # Create an invalid DataFrame for testing
        data = {
            KEY_VOXEL: [1, 1, 2, 3],
            KEY_MATERIAL: [10, 20, 10, 40],
            KEY_CELL: [11, 12, 11, 14],
            "MASS [kg]": [2.34, 3.13, 1.09, 10.2],  # Incorrect column name
        }
        df = pd.DataFrame(data)
        df.set_index([KEY_VOXEL, KEY_MATERIAL, KEY_CELL], inplace=True)

        # Verify that initializing the validator raises a ValueError
        with self.assertRaises(ValueError):
            DataMass(df)

    def test_get_filtered_dataframe_by_voxels_and_materials(self):
        # Expected dataframe
        data = {
            KEY_VOXEL: [1],
            KEY_MATERIAL: [20],
            KEY_CELL: [12],
            KEY_MASS_GRAMS: [3.13],
        }
        expected_df = pd.DataFrame(data)
        expected_df.set_index([KEY_VOXEL, KEY_MATERIAL, KEY_CELL], inplace=True)

        filtered_df = self.data_mass.get_filtered_dataframe(
            voxels=[1, 2], materials=[20, 40]
        )
        self.assertTrue(filtered_df.equals(expected_df))

    def test_get_cells_from_materials(self):
        cells = self.data_mass.get_cells_from_materials(materials=[10, 20])
        self.assertListEqual([11, 12], cells)
