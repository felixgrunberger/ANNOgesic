import os
import unittest
import shutil
import sys
sys.path.append(".")
from annogesiclib.paths import Paths


class TestPaths(unittest.TestCase):

    def setUp(self):
        self.test_folder = "test_folder"
        if not os.path.exists(self.test_folder):
            os.mkdir(self.test_folder)
        self.paths = Paths(base_path=self.test_folder)
        self.folder_names = [
            self.paths.input_folder,
            self.paths.output_folder,
            self.paths.reference_input_folder,
            self.paths.wig_folder,
            self.paths.mutation_table_folder,
            self.paths.database_folder,
            self.paths.manual_TSS_folder,
            self.paths.manual_pro_folder,
            self.paths.read_folder,
            self.paths.bam_folder,
            self.paths.target_folder,
            self.paths.ratt_folder,
            self.paths.tsspredator_folder,
            self.paths.utr_folder,
            self.paths.transterm_folder,
            self.paths.transcript_assembly_output_folder,
            self.paths.processing_site_folder,
            self.paths.srna_folder,
            self.paths.sorf_folder,
            self.paths.promoter_output_folder,
            self.paths.operon_output_folder,
            self.paths.circrna_output_folder,
            self.paths.goterm_output_folder,
            self.paths.starget_output_folder,
            self.paths.snp_output_folder,
            self.paths.ppi_output_folder,
            self.paths.sublocal_output_folder,
            self.paths.ribos_output_folder]

    def tearDown(self):
        if os.path.exists(self.test_folder):
            shutil.rmtree(self.test_folder)

    def test_set_folder_names(self):
        self.paths._set_folder_names()
        for folder_name in self.folder_names:
            assert(folder_name != '')
            self.assertEqual(self.folder_names.count(folder_name), 1)


    def test_required_folders(self):
        self.assertEqual(len(self.paths.required_folders("root")), 21)
        self.assertEqual(len(self.paths.required_folders("get_target_fasta")), 24)
        self.assertEqual(len(self.paths.required_folders("TSS")), 26)
        self.assertEqual(len(self.paths.required_folders("transcript_assembly")), 25)
        self.assertEqual(len(self.paths.required_folders("terminator")), 26)
        self.assertEqual(len(self.paths.required_folders("annotation_transfer")), 24)
        self.assertEqual(len(self.paths.required_folders("utr")), 28)
        self.assertEqual(len(self.paths.required_folders("promoter")), 22)
        self.assertEqual(len(self.paths.required_folders("operon")), 25)
        self.assertEqual(len(self.paths.required_folders("srna")), 36)
        self.assertEqual(len(self.paths.required_folders("sorf")), 29)
        self.assertEqual(len(self.paths.required_folders("processing")), 26)
        self.assertEqual(len(self.paths.required_folders("riboswitch")), 26)
        self.assertEqual(len(self.paths.required_folders("go_term")), 28)
        self.assertEqual(len(self.paths.required_folders("ppi_network")), 25)
        self.assertEqual(len(self.paths.required_folders("circrna")), 27)
        self.assertEqual(len(self.paths.required_folders("snp")), 38)
        self.assertEqual(len(self.paths.required_folders("subcellular_localization")), 28)
        self.assertEqual(len(self.paths.required_folders("srna_target")), 27)

if __name__ == "__main__":
    unittest.main()    
