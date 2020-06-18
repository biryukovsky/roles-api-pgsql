from marshmallow import Schema, post_dump


class Base(Schema):
    missing_fields = []

    @post_dump
    def remove_skip_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items()
            if self._validate_none_fields(key, value)
        }

    def _validate_none_fields(self, key, value):
        if value is not None or key not in self._get_none_fields():
            return True

    def _get_none_fields(self):
        missing_fields = []
        for k, v in self.fields.items():
            if not v.required:
                missing_fields.append(k)
        return missing_fields


class BaseEntity:
    def make_dump(self):
        return self.Schema().dump(self)

    @staticmethod
    def Schema():
        pass