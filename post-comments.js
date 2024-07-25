async function postCommentToGitHub(comment_body, commit_id, file_path, start_line, side) {
  const { Octokit } = await import('@octokit/core');

  try {
    const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

    console.log('Arguments:', { comment_body, commit_id, file_path, start_line, side });

    const [owner, repo] = process.env.GITHUB_REPOSITORY.split('/');
    const pull_number = process.env.GITHUB_EVENT_NUMBER;

    console.log('Repository Info:', { owner, repo, pull_number });

    const response = await octokit.request('POST /repos/{owner}/{repo}/pulls/{pull_number}/comments', {
      owner,
      repo,
      pull_number,
      commit_id,
      path: file_path,
      body: comment_body,
      position: parseInt(start_line, 3),
    });

    if (response.status !== 201) {
      throw new Error(`GitHub API responded with ${response.status}: ${response.statusText}`);
    }

    console.log('Comment posted successfully:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error posting comment:', error.message);
    console.error(error);
  }
}

const args = process.argv.slice(2);

if (args.length < 5) {
  console.error('Insufficient arguments. Expected: comment_body, commit_id, file_path, start_line, side');
  process.exit(1);
}

const [comment_body, commit_id, file_path, start_line, side] = args;

postCommentToGitHub(comment_body, commit_id, file_path, start_line, side)
  .then(response => console.log('Comment posted successfully:', response))
  .catch(error => console.error('Error posting comment:', error));
