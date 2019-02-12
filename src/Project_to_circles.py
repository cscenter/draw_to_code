from geometry import Point, Segment


def last_changes(final_list_of_segments, final_list_of_circles):
    new_segments = []
    for Seg in final_list_of_segments:
        P1 = Seg.point_1
        P2 = Seg.point_2
        EPSSS = 10
        p1x = P1.x
        p1y = P1.y
        p2x = P2.x
        p2y = P2.y
        P1_new = Point(p1x, p1y)
        P2_new = Point(p2x, p2y)
        k1 = False
        k2 = False
        for circle in final_list_of_circles:
            radius_ = circle.radius
            center_ = circle.center
            distt1 = Point.distance_between(P1, center_)
            if abs(distt1 - radius_) < EPSSS:
                P1_new = circle.project_point_seg(Seg, P1)
                k1 = True
            distt2 = Point.distance_between(P2, center_)
            if abs(distt2 - radius_) < EPSSS:
                P2_new = circle.project_point_seg(Seg, P2)
                k2 = True
            if k1 and k2:
                break
        new_segments.append(Segment(P1_new, P2_new))
    return new_segments


def unite_similar(final_list_of_segments):
    current_points = []
    THRES = 18
    new_list = []
    for Seg in final_list_of_segments:
        keyy1 = False
        keyy2 = False
        PP1 = Seg.point_1
        PP2 = Seg.point_2
        for curP in current_points:
            if Point.distance_between(PP1, curP) < THRES:
                Seg.point_1.x = curP.x
                Seg.point_1.y = curP.y
                keyy1 = True
            if Point.distance_between(PP2, curP) < THRES:
                Seg.point_2.x = curP.x
                Seg.point_2.y = curP.y
                keyy2 = True
        if not keyy1:
            current_points.append(PP1)
        if not keyy2:
            current_points.append(PP2)
        new_list.append(Seg)
    return new_list


def normalize(size, final_list_of_segments, final_list_of_circles):
    size /= 20
    for i in range(len(final_list_of_segments)):
        final_list_of_segments[i].point_1.x /= size
        final_list_of_segments[i].point_1.y /= size
        final_list_of_segments[i].point_2.x /= size
        final_list_of_segments[i].point_2.y /= size
    for i in range(len(final_list_of_circles)):
        final_list_of_circles[i].center.x /= size
        final_list_of_circles[i].center.y /= size
        final_list_of_circles[i].radius /= size
    return (final_list_of_segments, final_list_of_circles)
