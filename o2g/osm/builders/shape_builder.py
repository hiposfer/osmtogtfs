"""Functionality to build a list of shapes."""
import logging

from o2g.osm.models import Shape


def build_shapes(relations, nodes, ways):
    for rel in relations.values():
        for record in build_shape(rel, nodes, ways):
            if record:
                yield record


def build_shape(relation, nodes, ways):
    """Extract shape of one route."""
    sequence_index = 0

    for member_type, member_id, member_role in relation.member_info:

        if member_id in nodes:
            yield Shape(
                relation.id,
                nodes[member_id].lat,
                nodes[member_id].lon,
                sequence_index)

            sequence_index += 1

        # Do we need to consider ways too? It dramatically increases the number of shapes.
        elif member_id in ways:
            continue
        #     for point in ways[member_id].points:
        #         shape = Shape(
        #             relation.id,
        #             point.lat,
        #             point.lon,
        #             sequence_index)
        #         sequence_index += 1

        else:
            # Ignore excessive logging for now.
            pass
            # if member_type == 'n':
            #     member_osm_type = 'node'
            # elif member_type == 'w':
            #     member_osm_type = 'way'
            # else:
            #     member_osm_type = member_type
            # logging.warning('[no data] https://osm.org/relation/%s missing https://osm.org/%s/%s.',
            #                 relation.id, member_osm_type, member_id)
