import sys
import pandas as pd
import requests
from unidecode import unidecode
from datetime import datetime

# --- Local imports ---
from collaborator import Collaborator
from issue import Issue
from log import LOG, print_log
from sync import Sync
from anytype import TAG_DICT

def get_date_from_brazilian_format(date_str: str):
    """
    Converts a date string from Brazilian format (dd/mm/yyyy) to a datetime object.
    """
    meses_pt = {
        'jan': '01', 'fev': '02', 'mar': '03', 'abr': '04', 
        'mai': '05', 'jun': '06', 'jul': '07', 'ago': '08', 
        'set': '09', 'out': '10', 'nov': '11', 'dez': '12'
    }
    try:
        date_str = date_str.lower()
        for mes_pt, mes_num in meses_pt.items():
            date_str = date_str.replace(mes_pt, mes_num)
        return pd.to_datetime(date_str, dayfirst=True).tz_localize('GMT0')
    except Exception as e:
        raise BaseException(f"Error parsing date '{date_str}': {e}")

def sync_csv_to_anytype(csv_path: str, force_update: bool = False):
    """
    Reads the CSV and orchestrates the verification, creation, or update.
    """
    # 1. Read CSV using pandas
    try:
        df = pd.read_csv(csv_path,encoding="utf-8")
    except FileNotFoundError:
        print_log(f"Error: Could not find the file {csv_path}")
        return

    print_log(f"Found {len(df)} issues in CSV. Starting sync...")
    for index, row in df.iterrows():
        print_log(f" - {row.get('Chave da item', 'N/A')}: {row.get('Resumo', 'N/A')} ")
    
    # 2. Reads colaborators form Anytype
    print_log(f"Found {len(Collaborator.COLLABORATORS)} collaborators in Anytype.")
    print_log("Collaborators: \n", Collaborator.COLLABORATORS)
    
    skip_count, update_count, create_count, error_count = 0, 0, 0, 0
    
    #Issues created and updated in this sync session
    issues = []
    
    # 3. Iterate through the rows
    # Assuming CSV has columns: Title, Description, Status, Tipo de item,
    # Chave da item, Responsável, Campo personalizado (Tester), Resumo, Relator
    print_log("\nProcessing issues...")
    for index, row in df.iterrows():
        tipo = str(row.get('Tipo de item', ''))
        chave = str(row.get('Chave da item', ''))
        responsavel = " ".join(str(row.get('Responsável', '')).split(" ")[:2])
        tester = str(row.get('Campo personalizado (Tester)', ''))
        resumo = str(row.get('Resumo', ''))
        relator = str(row.get('Relator', ''))
        status = str(row.get('Status', ''))
        last_updated = get_date_from_brazilian_format(str(row.get('Atualizado(a)', '')))
        sprints = []
        
        desenvolverdores = []
        desenvolverdores_title = "Campo personalizado (Desenvolvedor)"
        count = 1
        while desenvolverdores_title in row:
            desenvolverdores = [str(dev) for dev in str(row.get(desenvolverdores_title, '')).split(",") if str(dev).strip()]
            count += 1
            desenvolverdores_title = f"Campo personalizado (Desenvolvedor)_{count}"
        
        if responsavel != '':
            desenvolverdores.append(responsavel)
        
        # Dynamically read sprint columns (Sprint, Sprint.1, Sprint.2, etc.) until an empty value is found
        count = 0
        aux = ''
        while str(row.get('Sprint' + aux, '')) not in ['', 'nan']:
            key = str(row.get('Sprint' + aux, ''))
            sprints.append(TAG_DICT.get(key, 'unknown'))
            count += 1
            aux = f".{count}"
        
        print_log(f"\nProcessing: [{', '.join(sprints)}] {chave} - {resumo}")
        
        # 3. Verify if tracked
        issue = Issue.get_issue_by_title(chave)
        
        print_log(f" ID: {issue.object_id}")
        try:
            if issue is not None:
                # 4a. Update tracked issue if update is latter than last update in Anytype
                print_log(f" Found existing issue. Updating...")
                if issue.last_updated and last_updated and last_updated <= issue.last_updated and not force_update:
                    print_log(" Issue is up to date. Skipping update.")
                    skip_count += 1
                else:
                    issue.update_issue(sprints, status, chave, tipo, desenvolverdores, tester, resumo, relator, force_update)
                    print_log(" Update successful.")
                    update_count += 1
            else:
                # 4b. Create untracked issue
                print_log(" Issue not found in Anytype. Creating new object...")
                issue =Issue(sprints, status, chave, tipo, desenvolverdores, tester, resumo, relator)
                print_log(" Creation successful.")
                create_count += 1
        
            issues.append(issue)        
        except requests.exceptions.RequestException as e:
            print_log(f" API > Issue Error processing '{chave}': `{e}`")
            print_log(f" Payload: {e.request.body}")
            error_count += 1

    print_log(f"\nSync completed. Summary:")
    print_log(f" - Updated: {update_count}")
    print_log(f" - Created: {create_count}")
    print_log(f" - Errors: {error_count}")
    print_log(f" - Skipped (up to date): {skip_count}")
    
    _ = Sync(csv_path, issues, LOG, skip_count, update_count, create_count, error_count)

if __name__ == "__main__":
    args = sys.argv[1:]
    force_update = False
    
    # Ensure collaborators are listed and available for lookup
    Collaborator.list_collaborators()
    
    if args:
        for input in args:
            if input in ["-f", "--force"]:
                force_update = True
            else:
                file = input.strip()
                print_log(f"Starting sync for: {file}")
                sync_csv_to_anytype(file,force_update)
    else:
        print_log("Starting sync...")
        file = input("Enter the path to the CSV file (e.g., issues_data.csv): ")
        file = file if file else "issues_data.csv"
        print_log(f"Using file: {file}")
        sync_csv_to_anytype(file,force_update)