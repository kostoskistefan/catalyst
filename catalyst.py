#!/usr/bin/python

import os
import shutil
import pathlib
import argparse
import datetime


catalyst_directory = pathlib.Path(__file__).parent.resolve()


def parse_arguments() -> list:
    parser = argparse.ArgumentParser(description='Generate a new C project')

    required_group = parser.add_argument_group('required arguments')
    optional_group = parser.add_argument_group('optional arguments')

    required_group.add_argument('--name', type=str, required=True, help='The name of the project')
    optional_group.add_argument('--type', type=str, default='executable', required=False, choices = ['executable', 'library'], help='The type of the project to generate')
    optional_group.add_argument('--enable-tests', type=str, default='false', required=False, choices = ['true', 'false'], help='Whether to generate tests')
    optional_group.add_argument('--license', type=str, default='MIT', required=False, choices = ['MIT', 'GPL'], help='The license of the project')

    arguments = parser.parse_args()

    return {
        'project_name_hyphen': arguments.name.replace('_', '-').replace(' ', '-').lower(),
        'project_name_underscore': arguments.name.replace('-', '_').replace(' ', '_').lower(),
        'project_type': arguments.type,
        'project_tests_enabled': arguments.enable_tests,
        'project_license': arguments.license
    }


def create_directory_structure(args):
    if not os.path.isdir('source'):
        os.mkdir('source')

    if args['project_type'] == 'library':
        if not os.path.isdir('include'):
            os.mkdir('include')

    if args['project_tests_enabled'] == 'true':
        if not os.path.isdir('test'):
            os.mkdir('test')


def generate_files(args):
    project_type = args['project_type'][0:3]

    # Meson files
    shutil.copyfile(catalyst_directory / str('meson.build.' + project_type + '_template'), 'meson.build')
    shutil.copyfile(catalyst_directory / 'meson.options', 'meson.options')

    # Clang format file
    shutil.copyfile(catalyst_directory / '.clang-format', '.clang-format')

    # Source file
    shutil.copyfile(catalyst_directory / str(args['project_license'].lower() + '_template.txt'), 'source/' + args['project_name_underscore'] + '.c')

    # Header file
    if args['project_type'] == 'library':
        shutil.copyfile(catalyst_directory / str(args['project_license'].lower() + '_template.txt'), 'include/' + args['project_name_underscore'] + '.h')

    # Tests file
    if args['project_tests_enabled'] == 'true':
        shutil.copyfile(catalyst_directory / str(args['project_license'].lower() + '_template.txt'), 'test/' + args['project_name_underscore'] + '.c')


def replace_template_definitions_in_files(args):
    # Meson build file
    file = pathlib.Path(r"meson.build") 
  
    data = file.read_text() 
    data = data.replace("$$PROJECT_NAME$$", args['project_name_underscore']) 
    data = data.replace("$$PROJECT_NAME_HYPHEN$$", args['project_name_hyphen']) 
    data = data.replace("$$PROJECT_LICENSE$$", args['project_license']) 
  
    file.write_text(data)  

    # Meson options file
    file = pathlib.Path(r"meson.options") 
  
    data = file.read_text() 
    data = data.replace("$$PROJECT_TESTS_ENABLED$$", args['project_tests_enabled']) 
  
    file.write_text(data)  

    # Source file
    file = pathlib.Path(r"source/" + args['project_name_underscore'] + ".c") 
  
    data = file.read_text() 
    data = data.replace("$$FILE_NAME$$", args['project_name_underscore'] + ".c") 
    data = data.replace("$$FILE_DATE$$", datetime.date.today().strftime("%d %B %Y")) 

    if args['project_type'] == 'executable':
        data += pathlib.Path(catalyst_directory / "exe_template.c").read_text()

    else:
        data += pathlib.Path(catalyst_directory / "lib_template.c").read_text().replace("$$PROJECT_NAME$$", args['project_name_underscore'])
  
    file.write_text(data)  

    # Header file
    if args['project_type'] == 'library':
        file = pathlib.Path(r"include/" + args['project_name_underscore'] + ".h") 
      
        data = file.read_text() 
        data = data.replace("$$FILE_NAME$$", args['project_name_underscore'] + ".h") 
        data = data.replace("$$FILE_DATE$$", datetime.date.today().strftime("%d %B %Y")) 
        data += "#pragma once\n\n"
      
        file.write_text(data)  

    # Test file
    if args['project_tests_enabled'] == 'true':
        file = pathlib.Path(r"test/" + args['project_name_underscore'] + ".c") 
      
        data = file.read_text() 
        data = data.replace("$$FILE_NAME$$", args['project_name_underscore'] + ".c") 
        data = data.replace("$$FILE_DATE$$", datetime.date.today().strftime("%d %B %Y")) 

        if args['project_type'] == 'library':
            data += "#include \"../include/" + args['project_name_underscore'] + ".h\"\n"

        data += pathlib.Path(catalyst_directory / "test_template.c").read_text()
      
        file.write_text(data)  


if __name__ == '__main__':
    args = parse_arguments()

    create_directory_structure(args)
    generate_files(args)
    replace_template_definitions_in_files(args)
