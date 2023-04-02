import unittest
import asyncio
from pars_qitea_tz import get_file_hash, main, file_name_list
import os


class TestGetContent(unittest.TestCase):

    def setUp(self):
        self.count = 3
        self.content = os.listdir('data')
        self.count_file = len(self.content)
        self.url1 = 'https://gitea.radium.group/radium/project-configuration'
        asyncio.run(main(count=self.count, url=self.url1))
        self.file_hash_data = {i: get_file_hash(i) for i in file_name_list}

    def test_add_files(self):
        """
        Проверяет количество добавленных файлов.
        Должно равняться количеству запросов self.count
        """
        new_count_file = len(os.listdir('data'))
        self.assertTrue(new_count_file - self.count_file == self.count)

    def test_hash_files(self):
        """
        Проверяет правильность расчета hash для новых файлов
        """
        new_content = [i for i in os.listdir('data') if i not in self.content]
        for i in range(self.count):
            new_key = get_file_hash("data/" + new_content[i])
            old_key = self.file_hash_data["data/" + new_content[i]]
            self.assertTrue(new_key == old_key)
