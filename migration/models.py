from pydantic import BaseModel
from typing import Literal, List


class Credentials(BaseModel):
    username: str
    password: str
    domain: str


class MountPoint(BaseModel):
    mount_point_name: str
    total_size: int


class Workload(BaseModel):
    ip: str
    credentials: Credentials
    storage: List[MountPoint]


class MigrationTarget(BaseModel):
    cloud_type: Literal['aws', 'azure', 'vsphere', 'vcloud']
    cloud_credentials: Credentials
    target_vm: Workload


class Migration(BaseModel):
    selected_mount_points: List[MountPoint]
    source: Workload
    migration_target: MigrationTarget
    migration_state: Literal['not_started', 'running', 'error', 'success'] = 'not_started'


# class Store(BaseModel):
#     credentials: list[Credentials]
#     mount_points: list[MountPoint]
#     workloads: list[Workload]
#     migration_targets: list[MigrationTarget]
#     migrations: list[Migration]
