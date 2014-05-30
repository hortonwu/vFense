from vFense.server.hierarchy import GroupKey


class Group():

    def __init__(
        self,
        group_name,
        view,
        permissions=[],
        group_id=None
    ):

        self.id = group_id

        self.group_name = group_name
        self.view = view

        self.permissions = permissions

    def add_permission(self, permission):

        if permission not in self.permissions:
            self.permissions.append(permission)

    def remove_permission(self, permission):

        if permission in self.permissions:
            self.permissions.remove(permission)

    def set_permissions(self, permissions):

        self.permissions = permissions

    def set_view(self, view_name):

        self.view = view_name

    def dict(self):

        return {
            GroupKey.Id: self.id,
            GroupKey.GroupName: self.group_name,
            GroupKey.Permissions: self.permissions,
            GroupKey.ViewId: self.view
        }

    def __repr__(self):

        return (
            "Group(name=%r,id=%r, view=%r)"
            % (self.group_name, self.id, self.view)
        )
