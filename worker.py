import asyncio

import mistralai.workflows as workflows

from tischlerei.workflows.report import TischlereiReportWorkflow


async def main():
    await workflows.run_worker([TischlereiReportWorkflow])


if __name__ == "__main__":
    asyncio.run(main())
