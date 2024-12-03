Don't forget:
```bash
export PATH="$HOME/scripts:$PATH"
```

In your `~/.zshrc` or `~/.bashrc` file

# `vmanage` docs — VM vCPU management script

`vmanage` is a Bash script for managing virtual machine (VM) CPU configurations using `virsh` under the hood.
It supports customized vCPU pinning and periodic migration operations for vCPUs.

> [!WARNING]
> Make sure to run `vmanage` as root (with `sudo`)

## Features
- Interactive Mode: Guided prompts to configure vCPU pinning or migration.
- Command-line Mode: Direct execution with arguments.
- vCPU Pinning: Pin vCPUs to specific physical CPUs or sockets.
- vCPU Migration: Periodically migrate vCPUs between physical cores.
- Hardware Topology Awareness: Detects CPU, core, and thread relationships.

## Usage

### Interactive Mode

Run the script interactively:
```bash
sudo ./vmanage -i
```

### Command-line Mode (Direct Execution)

Execute operations directly:
```bash
sudo ./vmanage [options]
```

### Common Options

- `-d`, `--domain DOMAIN` : VM domain name.
- `-o`, `--operation OP` : Operation (vcpupin or migrate).
- `-s`, `--socket SOCKET` : Socket number.
- `--vcpu VCPU_NUM` : vCPU number to migrate.
- `--core1 CORE` : First physical core.
- `--core2 CORE` : Second physical core.
- `--interval SECONDS` : Migration interval.
- `-h`, `--help` : Show help message.

## Examples

- Interactive Mode:
```bash
sudo ./vmanage -i
```

- Pin vCPUs to Socket 0:
```bash
sudo ./vmanage -d vm1 -o vcpupin -s 0
```

- Migrate vCPU between physical cores 0 and 4 every 60 seconds:
```bash
sudo ./vmanage -d vm1 -o migrate --vcpu 1 --core1 0 --core2 4 --interval 60
```

## Sample Outputs

- vCPU Pinning:
```bash
$ sudo ./vmanage -d vm1 -o vcpupin --distribute
[+] vCPU count for domain 'vm1': 4
[+] Pinned vCPU 0 to physical CPU 0
[+] Pinned vCPU 1 to physical CPU 1
[+] Pinned vCPU 2 to physical CPU 2
[+] Pinned vCPU 3 to physical CPU 3
[+] Equivalent command-line syntax:
vmanage -d vm1 -o vcpupin --distribute
```

- vCPU Migration:
```bash
$ sudo ./vmanage -d vm1 -o vcpupin --distribute
[+] vCPU count for domain 'vm1': 4
[+] Pinned vCPU 0 to physical CPU 0
[+] Pinned vCPU 1 to physical CPU 1
[+] Pinned vCPU 2 to physical CPU 2
[+] Pinned vCPU 3 to physical CPU 3
[+] Equivalent command-line syntax:
vmanage -d vm1 -o vcpupin --distribute
```


