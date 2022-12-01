import asana

from utils import (
    WOKRSPACE_FOLDER,
    PROJECTS_FOLDER,
    TASKS_FOLDER,
    ATTCHMENTS_FOLDER,
    COMMENTS_FOLDER,
    make_file_path,
    make_folder_path,
    save_to_json,
    initialize_folders,
    download_file
)


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


def get_subtasks(client, task_gid):
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
    attachment_detail = client.attachments.find_by_id(
        attachment=attachment_gid)

    return attachment_detail


def main():
    # create folders if missing
    initialize_folders()

    client = asana.Client.access_token('test-asana-peronsal-access-token')

    # Get workspaces
    workspaces = get_workspaces(client)

    # Get each workspace
    # workspaces_projcets = list()
    for workspace in workspaces:
        workspace_id = workspace["gid"]

        # Get and save workspace detail
        workspace_detail = get_workspace_detail(client, workspace_id)
        workspace_file_path = make_file_path(
            WOKRSPACE_FOLDER, f"{workspace_id}-workspace.json")

        save_to_json(workspace_file_path, workspace_detail)

    # Get projects of each workspace
    workspaces_projcets = list()
    for workspace in workspaces:
        workspace_id = workspace["gid"]
        workspace_projcets = get_projects(client, workspace_id)

        for project in workspace_projcets:
            project_id = project["gid"]
            project_folder_path = make_folder_path(
                PROJECTS_FOLDER, f"{workspace_id}-workspace")
            project_file_path = make_file_path(
                project_folder_path, f"{project_id}-project.json")

            project_detail = get_project_detail(client, project_id)

            save_to_json(project_file_path, project_detail)

        workspaces_projcets.extend(workspace_projcets)

    # Get task and subtask of each project
    all_tasks = list()
    for project in workspaces_projcets:
        project_id = project["gid"]
        project_tasks = get_project_tasks(client, project_id)

        project_folder_path = make_folder_path(
            TASKS_FOLDER, f"{project_id}-project")

        for task in project_tasks:
            task_id = task["gid"]
            task_file_path = make_file_path(
                project_folder_path, f"{task_id}-task.json")
            subtask_folder_path = make_folder_path(
                TASKS_FOLDER, f"{project_id}-project", f"{task_id}-subtasks")

            task_detail = get_task_detail(client, task_id)
            save_to_json(task_file_path, task_detail)

            # Get subtasks of task
            subtasks = get_subtasks(client, task_id)
            all_tasks.extend(subtasks)

            for subtask in subtasks:
                subtask_id = subtask["gid"]
                subtask_file_path = make_file_path(
                    subtask_folder_path, f"{subtask_id}-subtask.json")

                subtask_detail = get_task_detail(client, subtask_id)
                save_to_json(subtask_file_path, subtask_detail)

        all_tasks.extend(project_tasks)

    # Get attachments of each task
    for task in all_tasks:
        task_id = task["gid"]
        attachments_folder_path = make_folder_path(
            ATTCHMENTS_FOLDER, f"{task_id}-task")

        task_attachments = get_task_attachments(client, task_id)

        for attachment in task_attachments:
            attachment_id = attachment["gid"]
            attachment_file_path = make_file_path(
                attachments_folder_path, f"{attachment_id}-attachment.json")

            attachment_detail = get_attachment_detail(client, attachment_id)
            save_to_json(attachment_file_path, attachment_detail)

            # TODO: Download attachment
            # attachment_image_path = make_file_path(
            #     attachments_folder_path, f"{attachment_id}-attachment.png")
            # download_file(
            #     attachment_detail["download_url"], attachment_image_path)

    # Get comments of each task
    for task in all_tasks:
        task_id = task["gid"]
        comments_folder_path = make_folder_path(
            COMMENTS_FOLDER, f"{task_id}-task")
        comments_file_path = make_file_path(
            comments_folder_path, f"comments.json")

        comments = get_task_comments(client, task_id)
        save_to_json(comments_file_path, comments)


if __name__ == "__main__":
    main()
