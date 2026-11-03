from unittest.mock import MagicMock

import httpx

from end_to_end_tests.functional_tests.helpers import (
    assert_model_decode_encode,
    assert_model_property_type_hint,
    with_generated_client_fixture,
    with_generated_code_import,
    with_generated_code_imports,
)


@with_generated_client_fixture(
    """
components:
  schemas:
    StringOrInt:
      type: ["string", "integer"]
    MyModel:
      type: object
      properties:
        stringOrIntProp:
          type: ["string", "integer"]
"""
)
@with_generated_code_imports(
    ".models.MyModel",
)
class TestSimpleTypeList:
    def test_decode_encode(self, MyModel):
        assert_model_decode_encode(MyModel, {"stringOrIntProp": "a"}, MyModel(string_or_int_prop="a"))
        assert_model_decode_encode(MyModel, {"stringOrIntProp": 1}, MyModel(string_or_int_prop=1))

    def test_type_hints(self, MyModel):
        assert_model_property_type_hint(MyModel, "string_or_int_prop", "int | str | Unset")


@with_generated_client_fixture(
    """
components:
  schemas:
    ThingA:
      type: object
      properties:
        propA: { type: "string" }
      required: ["propA"]
    ThingB:
      type: object
      properties:
        propB: { type: "string" }
      required: ["propB"]
    ThingAOrB:
      oneOf:
        - $ref: "#/components/schemas/ThingA"
        - $ref: "#/components/schemas/ThingB"
    ModelWithUnion:
      type: object
      properties:
        thing: {"$ref": "#/components/schemas/ThingAOrB"}
        thingOrString:
          oneOf:
            - $ref: "#/components/schemas/ThingA"
            - type: string
    ModelWithRequiredUnion:
      type: object
      properties:
        thing: {"$ref": "#/components/schemas/ThingAOrB"}
      required: ["thing"]
    ModelWithNestedUnion:
      type: object
      properties:
        thingOrValue:
          oneOf:
            - "$ref": "#/components/schemas/ThingAOrB"
            - oneOf:
              - type: string
              - type: number
    ModelWithUnionOfOne:
      type: object
      properties:
        thing:
          oneOf:
            - $ref: "#/components/schemas/ThingA"
        requiredThing:
          oneOf:
            - $ref: "#/components/schemas/ThingA"
      required: ["requiredThing"]
"""
)
@with_generated_code_imports(
    ".models.ThingA",
    ".models.ThingB",
    ".models.ModelWithUnion",
    ".models.ModelWithRequiredUnion",
    ".models.ModelWithNestedUnion",
    ".models.ModelWithUnionOfOne",
)
class TestOneOf:
    def test_disambiguate_objects_via_required_properties(self, ThingA, ThingB, ModelWithUnion):
        assert_model_decode_encode(
            ModelWithUnion,
            {"thing": {"propA": "x"}},
            ModelWithUnion(thing=ThingA(prop_a="x")),
        )
        assert_model_decode_encode(
            ModelWithUnion,
            {"thing": {"propB": "x"}},
            ModelWithUnion(thing=ThingB(prop_b="x")),
        )

    def test_disambiguate_object_and_non_object(self, ThingA, ModelWithUnion):
        assert_model_decode_encode(
            ModelWithUnion,
            {"thingOrString": {"propA": "x"}},
            ModelWithUnion(thing_or_string=ThingA(prop_a="x")),
        )
        assert_model_decode_encode(
            ModelWithUnion,
            {"thingOrString": "x"},
            ModelWithUnion(thing_or_string="x"),
        )

    def test_disambiguate_nested_union(self, ThingA, ThingB, ModelWithNestedUnion):
        assert_model_decode_encode(
            ModelWithNestedUnion,
            {"thingOrValue": {"propA": "x"}},
            ModelWithNestedUnion(thing_or_value=ThingA(prop_a="x")),
        )
        assert_model_decode_encode(
            ModelWithNestedUnion,
            {"thingOrValue": 3},
            ModelWithNestedUnion(thing_or_value=3),
        )

    def test_type_hints(self, ModelWithUnion, ModelWithRequiredUnion, ModelWithUnionOfOne, ThingA):
        assert_model_property_type_hint(
            ModelWithUnion,
            "thing",
            "ThingA | ThingB | Unset",
        )
        assert_model_property_type_hint(
            ModelWithRequiredUnion,
            "thing",
            "ThingA | ThingB",
        )
        assert_model_property_type_hint(ModelWithUnionOfOne, "thing", "ThingA | Unset")
        assert_model_property_type_hint(ModelWithUnionOfOne, "required_thing", "ThingA")


@with_generated_client_fixture(
    """
paths:
  "/thing":
    get:
      operationId: getThing
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/InlineThingAOrB"
components:
  schemas:
    InlineThingAOrB:
      oneOf:
        - type: object
          properties:
            propA:
              type: object
              properties:
                value: {"$ref": "#/components/schemas/Value"}
          required: ["propA"]
        - type: object
          properties:
            propB:
              type: object
              properties:
                inner:
                  type: object
                  properties:
                    value: {"$ref": "#/components/schemas/Value"}
          required: ["propB"]
    Value:
      type: object
      properties:
        x: {"type": "string"}
"""
)
@with_generated_code_imports(
    ".models.InlineThingAOrBType0",
    ".models.InlineThingAOrBType0PropA",
    ".models.InlineThingAOrBType1",
    ".models.InlineThingAOrBType1PropB",
    ".models.InlineThingAOrBType1PropBInner",
    ".models.Value",
)
@with_generated_code_import(".api.default.get_thing.sync")
@with_generated_code_import(".client.Client")
class TestOneOfInlineObjectsWithInlineObjects:
    def test_decode_encode(
        self,
        InlineThingAOrBType0,
        InlineThingAOrBType0PropA,
        InlineThingAOrBType1,
        InlineThingAOrBType1PropB,
        InlineThingAOrBType1PropBInner,
        Value,
    ):
        assert_model_decode_encode(
            InlineThingAOrBType0,
            {"propA": {"value": {"x": "a"}}},
            InlineThingAOrBType0(prop_a=InlineThingAOrBType0PropA(value=Value(x="a"))),
        )
        assert_model_decode_encode(
            InlineThingAOrBType1,
            {"propB": {"inner": {"value": {"x": "b"}}}},
            InlineThingAOrBType1(
                prop_b=InlineThingAOrBType1PropB(inner=InlineThingAOrBType1PropBInner(value=Value(x="b")))
            ),
        )

    def test_disambiguate_response(self, sync, Client, InlineThingAOrBType1):
        mock_httpx_client = MagicMock(spec=httpx.Client)
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"propB": {"inner": {"value": {"x": "b"}}}}
        mock_response.content = b'{"propB": {"inner": {"value": {"x": "b"}}}}'
        mock_response.headers = {}
        mock_httpx_client.request.return_value = mock_response

        client = Client(base_url="https://api.example.com")
        client.set_httpx_client(mock_httpx_client)

        result = sync(client=client)

        assert isinstance(result, InlineThingAOrBType1)
        assert result.prop_b.inner.value.x == "b"
