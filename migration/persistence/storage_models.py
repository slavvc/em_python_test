from pydantic import BaseModel
from typing import List, Literal


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
    target_vm: int


class Migration(BaseModel):
    selected_mount_points: List[MountPoint] = []
    source: int
    migration_target: MigrationTarget
    migration_state: Literal['not_started', 'running', 'error', 'success'] = 'not_started'
