import asana


def get_workspaces(client):
    workspaces = list()
    for workspace in client.workspaces.get_workspaces():
        workspaces.append(workspace)

    return workspaces

def get_workspace_detail(client, workspace_gid):
    workspace_details = client.workspaces.find_by_id(workspace=workspace_gid)

    return workspace_details


def get_projects(client, workspace_gid):
    projects = list()
    for project in client.projects.get_projects(workspace=workspace_gid):
        projects.append(project)

    return projects


def get_project_detail(client, project_gid):
    project_details = client.projects.find_by_id(project=project_gid)

    return project_details


def get_project_tasks(client, project_gid):
    project_tasks = list()
    for task in client.tasks.find_by_project(project=project_gid):
        project_tasks.append(task)

    return project_tasks


def get_task_subtasks(client, task_gid):
    subtasks = list()
    for subtask in client.tasks.subtasks(task=task_gid):
        subtasks.append(subtask)

    return subtasks


def get_task_comments(client, task_gid):
    comments = list()
    for story in client.tasks.stories(task=task_gid):
        if story["type"] == "comment":
            comments.append(story)

    return comments


def get_task_detail(client, task_gid):

    task_details = client.tasks.find_by_id(task=task_gid)

    return task_details


def get_task_attachments(client, task_gid):
    attachments = list()
    for attachment in client.attachments.find_by_task(task=task_gid):
        attachments.append(attachment)

    return attachments

def get_attachment_detail(client, attachment_gid):
    attachment_detail = client.attachments.find_by_id(attachment=attachment_gid)

    return attachment_detail


def main():

    client = asana.Client.access_token(
        '1/41454015903126:4e3395944457c0fc42285ee7973c8f4c')

    # Get workspaces
    workspaces = get_workspaces(client)

    # Get projects for each workspace
    workspaces_projcets = list()
    for workspace in workspaces:
        workspace_id = workspace["gid"]
        workspace_projcets = get_projects(client, workspace_id)

        # save large list of all workspaces projects
        workspaces_projcets.extend(workspace_projcets)

    
    # Get task of each project
    for project in workspaces_projcets:
        project_id = project["gid"]
        project_tasks = get_project_tasks(client, project_id)

        for task in project_tasks:
            task_id = task["gid"]

            task_detail = get_task_detail(client, task_id)

            subtasks = get_task_subtasks(client, task_id)

    

if __name__ == "__main__":
    # main()
    client = asana.Client.access_token(
        '1/41454015903126:4e3395944457c0fc42285ee7973c8f4c')
    # workspace_detail = get_workspace_detail(client, "188866926275273")
    # print(workspace_detail)

    # project_detail = get_project_detail(client, "1203465472277766")
    # print(project_detail)

    # task_detail = get_task_detail(client, "1203465472277769")
    # print(task_detail)

    # task_comments = get_task_comments(client, "1203465472277769")
    # print(task_comments)

    attachment_gid = '1203465472277774'
    attachment_detail = get_attachment_detail(client, attachment_gid)
    print(attachment_detail)











# tasks = get_project_tasks(client, '1203465472277763')
# tasks = get_project_tasks(client, '1203465472277766')
# print(tasks)

# task_gid = '1203465472277769'

# task_detail = get_task_comments(client, task_gid)

# print(task_detail)


# task_subtasks = get_task_subtasks(client, task_gid)
# print(task_subtasks)

# get_task_detail(client, task_gid)


# task_attachments = get_task_attachments(client, task_gid)

# print(task_attachments)


# attachment_gid = '1203465472277790'
# attachment_gid = '1203465472277774'
# attachment_detail = get_attachment_detail(client, attachment_gid)
# print(attachment_detail)