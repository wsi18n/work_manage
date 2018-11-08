def init_permission(user, request):
    # 返回一个包含字典元素的列表,并且去重复
    permission_list = user.role.values("permission_title", "permission_url").dictinct()
    url_list = []
    # url权限列表
    for item in permission_list:
        url_list.append(item["permission_url"])
    # 将初始化的信息写入session
    request.session["permission_url_list"] = url_list
