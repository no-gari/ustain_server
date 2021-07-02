from drf_yasg.inspectors import SwaggerAutoSchema


class SquadSwaggerAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        tags = super().get_tags(operation_keys)

        if "api" in tags and operation_keys:
            # NOTE: `operation_keys` is a list like ["api", "v1", "token", "read"].
            tags[0] = operation_keys[2]
        return tags