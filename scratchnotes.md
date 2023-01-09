Scratch Workflow:

name: Run Add-On
on: repository_dispatch
jobs:
  Run-Add-On:
    uses: MuckRock/documentcloud-addon-workflows/.github/workflows/run-addon.yml@v1
    with:
      timeout: 60
    secrets: 
      muckrock_api)key: "${{ secrets.MUCKROCK_API_KEY }}"
      google_client_id: "${{ secrets.GOOGLE_CLIENT_ID }}"
      google_project_id: "${{ secrets.GOOGLE_PROJECT_ID }}"
      google_client_secret: "${{ secrets.GOOGLE_CLIENT_SECRET }}"
