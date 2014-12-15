from schematics.models import Model
from schematics.exceptions import (
        ConversionError,
        ModelValidationError,
        ValidationError,
)

from ...exceptions import ActionFieldError


class Action(Model):

    @classmethod
    def get_instance(action_klass, raw_data=None, deserialize_mapping=None, strict=True,
            **rpc_kwargs):
        rpc_kwargs = action_klass.pre_run(**rpc_kwargs)

        try:
            return action_klass(raw_data=rpc_kwargs,
                        deserialize_mapping=deserialize_mapping, strict=strict)
        except ConversionError, err:
            raise ActionFieldError(err)

    def execute_run(self, service):
        # now, after instantiation, fields will have been transformed and
        # computed based on rpc_kwargs inputs, which are the fields passed to
        # the service as kwargs.
        self._errors = []

        # validate input arguments
        if self.is_valid():
            action_kwargs = self.get_action_kwargs()
            self.run(**action_kwargs)

        # revalidate since the run method could have attached some new
        # attributes
        try:
            self.validate()
            final_results = self.finalize_results()
        except ModelValidationError, err:
            raise ActionFieldError(err)

        return final_results

    @classmethod
    def pre_run(klass, **kwargs):
        return kwargs

    def get_action_kwargs(self):
        return {}

    def add_error(self, msg, error_type, hint=''):
        self._errors.append({
            'error': msg,
            'error_type': error_type,
            'hint': hint})

    def get_errors(self):
        return self._errors

    def run(self, **kwargs):
        raise NotImplementedError('Clients must implement this method')

    def _response_names_and_fields_iter(self):
        for fieldname, field in self._fields.iteritems():
            if getattr(field, 'in_response', None):
                yield (fieldname, field)

    def finalize_results(self):
        """Grep out the final results/attributes the action should return."""
        results = {}
        for fieldname, field in self._response_names_and_fields_iter():
            value = getattr(self, fieldname)
            fieldname = field.serialized_name or fieldname
            results[fieldname] = field.to_native(value)

        return results

    def is_valid(self):
        if self._errors:
            return False

        try:
            self.validate()
            return True
        except ValidationError, err:
            self._errors = err.messages
            return False

    def handle_errors(self, **kwargs):
        return self._errors

