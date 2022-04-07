
import argparse

from . import maintainer



def parse_input():
    parser = argparse.ArgumentParser(description='Mini Version Sharing System')

    subparsers = parser.add_subparsers(dest='command', help='sub-command help')

    parser_init = subparsers.add_parser('init', help='initialize vss repository in  current dir')
    parser_init.add_argument('-f', '--force', action='store_true', help="force reinitialization even if something already exhist")
    parser_init.add_argument('--remote', help='set basic remote url')

    parser_show = subparsers.add_parser('show', help='show fixed versions')

    parser_add_platform = subparsers.add_parser('add_platform', help='add new platform to repository')
    parser_add_platform.add_argument('name', help='platform name')
    parser_add_platform.add_argument('working_file', help='file that will be fixed every version')

    parser_client_config = subparsers.add_parser('generate_client_config', help='create a python file with data for VSSClient inside an app')

    parser_add_version = subparsers.add_parser('fix', help='fix a new version')
    parser_add_version.add_argument('-p', '--platform', help='concrete platform to fix in')
    parser_add_version.add_argument('version_name', help='(semantic versioning)')

    args = parser.parse_args()
    if not args.command:
        print("You should specify action!\n")
        parser.print_help()
    return args


def main():
    args = parse_input()
    print(args)

    m = maintainer.VSSMaintainer()
    if args.command == 'init':
        maintainer.init_vss_folder(args.force)
    elif args.command == 'add_platform':
        m.add_platform(args.name, args.working_file)
    elif args.command == 'fix':
        m.add_version(args.version_name, args.platform)
    elif args.command == 'generate_client_config':
        m.generate_client_config_file("")
    elif args.command == 'show':
        for p in m.configs.platform_configs:
            print("Platform {}:".format(p.name))
            for v in p.platform.versions:
                print("\t- {}".format(v))
            # print("end\n")
