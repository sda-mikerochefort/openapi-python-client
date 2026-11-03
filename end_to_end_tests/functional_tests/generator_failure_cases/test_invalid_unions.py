from end_to_end_tests.functional_tests.helpers import assert_bad_schema, with_generated_client_fixture


@with_generated_client_fixture(
    """
components:
  schemas:
    UnionWithInvalidReference:
      anyOf:
        - $ref: "#/components/schemas/DoesntExist"
    UnionWithInvalidDefault:
      type: ["number", "integer"]
      default: aaa
    UnionWithMalformedVariant:
      anyOf:
        - type: string
        - type: array  # invalid because no items
    UnionWithInvalidInlineVariant:
      oneOf:
        - type: object
          properties:
            inner:
              type: object
              properties:
                invalidRef: {"$ref": "#/components/schemas/DoesntExist"}
        - type: string
    ModelWithInvalidUnion:
      type: object
      properties:
        union: {"$ref": "#/components/schemas/UnionWithInvalidInlineVariant"}
"""
)
class TestUnionInvalidSchemas:
    def test_invalid_reference(self, generated_client):
        assert_bad_schema(generated_client, "UnionWithInvalidReference", "Could not find reference")

    def test_invalid_default(self, generated_client):
        assert_bad_schema(generated_client, "UnionWithInvalidDefault", "Invalid int value: aaa")

    def test_invalid_property(self, generated_client):
        assert_bad_schema(generated_client, "UnionWithMalformedVariant", "Invalid property in union")

    def test_invalid_inline_variant(self, generated_client):
        # The union, and anything using it, is removed along with the invalid variant
        assert_bad_schema(
            generated_client,
            "UnionWithInvalidInlineVariant_type_0",
            "removal of:\n/components/schemas/UnionWithInvalidInlineVariant\n/components/schemas/ModelWithInvalidUnion",
        )
