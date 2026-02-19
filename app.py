from agents import build_researcher, build_writer
from tasks import research_task, write_task
from orchestrator import Orchestrator

def main():
    query = {
        "process": "Injection Molding",
        "material": ["ABS"],
        "location_preference": ["India"],
        "certifications": ["ISO 9001"],
        "monthly_capacity_min": 50000
    }

    researcher = build_researcher()
    writer = build_writer()
    
    orch = Orchestrator(
        researcher=researcher,
        writer=writer,
        research_task=research_task(researcher),
        write_task=write_task(writer)
    )

    result = orch.run(query)
    print(result)

if __name__ == "__main__":
    main()
