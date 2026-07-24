#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  MOTHERBRAIN — ShipWrekD OS Command Center
#  BleakNarratives / RootBase
#  For Sarah. The original.
# ═══════════════════════════════════════════════════════════════

ROOT="/storage/emulated/0/RootBase"
GRAB="/storage/emulated/0/GRAB"
ZIP="/storage/emulated/0/Zip"

# ── Colors ────────────────────────────────────────────────────
G="\033[38;5;118m"   # green
A="\033[38;5;214m"   # amber
C="\033[38;5;51m"    # cyan
R="\033[38;5;196m"   # red
M="\033[38;5;213m"   # magenta
W="\033[38;5;250m"   # ghost white
D="\033[38;5;240m"   # dim
B="\033[1m"          # bold
X="\033[0m"          # reset

# ── Header ────────────────────────────────────────────────────
header() {
clear
echo -e "${G}${B}"
cat << 'LOGO'
  ███╗   ███╗ ██████╗ ████████╗██╗  ██╗███████╗██████╗ 
  ████╗ ████║██╔═══██╗╚══██╔══╝██║  ██║██╔════╝██╔══██╗
  ██╔████╔██║██║   ██║   ██║   ███████║█████╗  ██████╔╝
  ██║╚██╔╝██║██║   ██║   ██║   ██╔══██║██╔══╝  ██╔══██╗
  ██║ ╚═╝ ██║╚██████╔╝   ██║   ██║  ██║███████╗██║  ██║
  ╚═╝     ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
     ██████╗ ██████╗  █████╗ ██╗███╗   ██╗               
     ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║               
     ██████╔╝██████╔╝███████║██║██╔██╗ ██║               
     ██╔══██╗██╔══██╗██╔══██║██║██║╚██╗██║               
     ██████╔╝██║  ██║██║  ██║██║██║ ╚████║               
     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝               
LOGO
echo -e "${X}${D}  ShipWrekD OS // BleakNarratives // For Sarah${X}"
echo -e "${D}  $(date '+%A %B %d %Y  %H:%M:%S')${X}"
echo ""
}

# ── Status bar ────────────────────────────────────────────────
status_bar() {
    # Check which providers have keys
    local ENV_FILE="$ROOT/Askhole-Too-Also/V3/.env"
    local CEREBRAS="✗" MISTRAL="✗" OPENROUTER="✗" GEMINI="✗" GROQ="✗"
    
    if [ -f "$ENV_FILE" ]; then
        grep -q "CEREBRAS_API_KEY=." "$ENV_FILE" && CEREBRAS="✓"
        grep -q "MISTRAL_API_KEY=."  "$ENV_FILE" && MISTRAL="✓"
        grep -q "OPENROUTER_API_KEY=." "$ENV_FILE" && OPENROUTER="✓"
        grep -q "GEMINI_API_KEY=."   "$ENV_FILE" && GEMINI="✓"
        grep -q "GROQ_API_KEY=."     "$ENV_FILE" && GROQ="✓"
    fi

    # Disk
    local DISK=$(df -h /storage/emulated/0 2>/dev/null | awk 'NR==2{print $4}')
    local ROOTSIZE=$(du -sh "$ROOT" 2>/dev/null | cut -f1)

    echo -e "${D}  ─────────────────────────────────────────────────────${X}"
    echo -e "  ${D}Providers:${X}  ${G}Cerebras${X}${D}:${X}$CEREBRAS  ${C}Mistral${X}${D}:${X}$MISTRAL  ${A}OpenRouter${X}${D}:${X}$OPENROUTER  ${W}Gemini${X}${D}:${X}$GEMINI  ${A}Groq${X}${D}:${X}$GROQ"
    echo -e "  ${D}RootBase:${X} ${W}$ROOTSIZE${X}   ${D}Free:${X} ${W}$DISK${X}"
    echo -e "${D}  ─────────────────────────────────────────────────────${X}"
    echo ""
}

# ── Menu renderer ─────────────────────────────────────────────
section() { echo -e "\n  ${A}${B}── $1 ──${X}"; }

item() {
    local KEY="$1" LABEL="$2" STATUS="$3" COLOR="${4:-$W}"
    printf "  ${G}%-4s${X} ${COLOR}%-32s${X} ${D}%s${X}\n" "[$KEY]" "$LABEL" "$STATUS"
}

main_menu() {
    header
    status_bar

    section "PITCH DAY — MORNING"
    item "1" "Yvette → Chew Plumbing"        "pitch ready // GRAB/Yvette/" "$G"
    item "2" "Countryside Motors pitch"        "GRAB/pitch_reports/" "$G"
    item "3" "RCB Bank pitch"                 "GRAB/pitch_reports/" "$G"
    item "4" "Travelin Smoke BBQ pitch"        "GRAB/pitch_reports/" "$A"

    section "VERTICAL AI — LIVE"
    item "5" "Official Boardroom (v1.4)"      "Official-Vertical-AI-Boardroom/" "$G"
    item "6" "Vertical Local (Flask)"         "vertical_local/run.sh" "$G"
    item "7" "AskHole V3"                     "Askhole-Too-Also/V3/" "$G"
    item "8" "Hotseat-Too"                    "Hotseat-Too/ // memory.db live" "$A"

    section "THE WORKBENCH"
    item "9" "CodeCity-Bench"                 "workbench.sh // Loom live" "$G"
    item "10" "CodeMentor MVP"                "backend/lib/ai_explain.py" "$A"
    item "11" "CaptCoder (AR cam app)"        "v1 + v2 // React/Vite" "$A"
    item "12" "Syntax AI Warden"              "syntax.py // multi-provider" "$G"

    section "INFRASTRUCTURE"
    item "13" "Lough Event Spine"             "lough_system/" "$G"
    item "14" "ZeroClaw Broker"               "zeroclaw_broker/server.py" "$A"
    item "15" "Mrs. Higgins SaaS"             "mrs_higgins_saas/" "$G"
    item "16" "Molt V4 Supervisor"            "Molt-V4/" "$A"
    item "17" "Thoth Orchestrator"            "thoth_orchestrator/thoth.py" "$A"

    section "WHORL ECOSYSTEM"
    item "18" "Whorl Runtime"                 "whorl_runtime.py // WHR" "$A"
    item "19" "Loom Weaver"                   "CodeCity-Bench/core/loom/" "$G"
    item "20" "Platform Bridge"               "whorl/platform_bridge/ STUB" "$D"
    item "21" "FORGE"                         "whorl/forge/ STUB" "$D"

    section "TOOLS"
    item "s"  "Syntax (quick chat)"           "python3 $ROOT/syntax.py" "$G"
    item "t"  "Tree scan"                     "tree_scan.sh" "$C"
    item "u"  "Update CONVERGENCE"            "open CONVERGENCE.md" "$C"
    item "g"  "GRIMOIRE shell"                "source grimoire.sh" "$C"
    item "q"  "Quit"                          "" "$R"

    echo ""
    echo -e -n "  ${G}${B}motherbrain>${X} "
}

# ── Launchers ─────────────────────────────────────────────────

launch_yvette() {
    echo -e "\n  ${G}${B}YVETTE — Chew Plumbing Demo${X}"
    echo -e "  ${D}────────────────────────────────${X}"
    echo -e "  ${W}Knowledge base:${X} $GRAB/Yvette/knowledge/plumbing_core.md"
    echo -e "  ${W}Pitch report:${X}   $GRAB/pitch_reports/Chew_Plumbing_pitch.txt"
    echo -e "  ${W}Outreach:${X}       $ROOT/Askhole-Too-Also/V3/outreach/"
    echo ""
    echo -e "  ${A}Pitch files:${X}"
    ls "$GRAB/pitch_reports/" 2>/dev/null | while read f; do
        echo -e "    ${D}→${X} $f"
    done
    echo ""
    echo -e "  ${G}Open pitch?${X} [y/n] "
    read -r yn
    if [[ "$yn" == "y" ]]; then
        cat "$GRAB/pitch_reports/Chew_Plumbing_pitch.txt" 2>/dev/null \
            || cat "$GRAB/pitch_reports/reports/Chew_Plumbing_pitch.txt" 2>/dev/null \
            || echo "  [!] Pitch file not found — check GRAB/pitch_reports/"
    fi
}

launch_boardroom() {
    echo -e "\n  ${G}Launching Official Vertical AI Boardroom...${X}"
    local DIR="$ROOT/Official-Vertical-AI-Boardroom"
    if [ -f "$DIR/runbook.txt" ]; then
        echo -e "  ${D}Runbook:${X}"
        head -20 "$DIR/runbook.txt"
    fi
    echo ""
    echo -e "  ${A}Run it? [y/n]${X} "
    read -r yn
    [[ "$yn" == "y" ]] && bash "$DIR/run.sh" 2>/dev/null \
        || python3 "$DIR/app.py" 2>/dev/null \
        || echo "  Check runbook for start command."
}

launch_vertical_local() {
    echo -e "\n  ${G}Launching Vertical Local (Flask)...${X}"
    cd "$ROOT/vertical_local" && bash run.sh
}

launch_askhole() {
    echo -e "\n  ${G}Launching AskHole V3...${X}"
    cd "$ROOT/Askhole-Too-Also/V3" && python3 askhole.py
}

launch_workbench() {
    echo -e "\n  ${G}Launching CodeCity-Bench...${X}"
    cd "$ROOT/CodeCity-Bench" && bash workbench.sh
}

launch_syntax() {
    echo -e "\n  ${G}Waking Syntax...${X}\n"
    python3 "$ROOT/syntax.py"
}

launch_tree() {
    echo -e "\n  ${G}Running tree scan...${X}"
    bash "$ROOT/tree_scan.sh" 2>/dev/null \
        || bash "/storage/emulated/0/Download/tree_scan.sh"
    echo -e "  ${D}Output: $ROOT/TREE_SNAPSHOT.txt${X}"
}

launch_lough() {
    echo -e "\n  ${G}Lough Event Spine${X}"
    local LOG="$ROOT/lough_system/lough.log"
    if [ -f "$LOG" ]; then
        echo -e "  ${D}Last 20 events:${X}"
        tail -20 "$LOG"
    else
        echo -e "  ${D}Log: $LOG${X}"
        ls "$ROOT/lough_system/" 2>/dev/null
    fi
}

launch_hotseat() {
    echo -e "\n  ${G}Launching Hotseat-Too...${X}"
    cd "$ROOT/Hotseat-Too" && python3 hotseat3.py 2>/dev/null \
        || ls . && echo "  Check runbook.txt for start command"
}

show_pitches() {
    local NAME="$1"
    echo -e "\n  ${G}${B}$NAME Pitch${X}"
    echo -e "  ${D}──────────────────────────────${X}"
    find "$GRAB/pitch_reports" -name "*${NAME}*" 2>/dev/null | while read f; do
        echo -e "\n  ${A}→ $f${X}"
        cat "$f"
    done
}

quick_syntax() {
    echo -e "\n  ${G}Syntax quick mode — type your question:${X}"
    echo -e -n "  ${G}>${X} "
    read -r Q
    python3 "$ROOT/syntax.py" "$Q"
}

grimoire() {
    echo -e "\n  ${G}Loading GRIMOIRE...${X}"
    source "$ROOT/shipwrekd_os/grimoire/grimoire.sh" 2>/dev/null \
        || echo -e "  ${D}Run: source $ROOT/shipwrekd_os/grimoire/grimoire.sh${X}"
}

# ── Main loop ─────────────────────────────────────────────────
while true; do
    main_menu
    read -r CHOICE

    case "$CHOICE" in
        1)  launch_yvette ;;
        2)  show_pitches "Countryside" ;;
        3)  show_pitches "RCB" ;;
        4)  show_pitches "Restaurant" ;;
        5)  launch_boardroom ;;
        6)  launch_vertical_local ;;
        7)  launch_askhole ;;
        8)  launch_hotseat ;;
        9)  launch_workbench ;;
        10) cd "$ROOT/CodeMentor-MVP" && python3 backend/lib/ai_explain.py 2>/dev/null || echo "  Check runbook.txt" ;;
        11) echo -e "\n  ${A}CaptCoder:${X} cd $ROOT/CaptCoder/v2 && npm run dev" ;;
        12) launch_syntax ;;
        13) launch_lough ;;
        14) cd "$ROOT/zeroclaw_broker/zeroclaw_lab_broker" && python3 -m zeroclaw_lab_broker.server 2>/dev/null || echo "  Check zeroclaw runbook" ;;
        15) cd "$ROOT/mrs_higgins_saas" && python3 front_desk_lady.py ;;
        16) cd "$ROOT/Molt-V4" && python3 molt.py 2>/dev/null || echo "  Check Molt-V4 runbook" ;;
        17) cd "$ROOT/thoth_orchestrator" && python3 thoth.py 2>/dev/null || echo "  Check thoth runbook" ;;
        18) echo -e "\n  ${A}Whorl:${X} python3 $ROOT/whorl_runtime.py" && python3 "$ROOT/whorl_runtime.py" ;;
        19) echo -e "\n  ${G}Loom is live in CodeCity-Bench${X}\n  ${D}$ROOT/CodeCity-Bench/src/core/loom/weaver.py${X}" ;;
        20) echo -e "\n  ${D}Platform Bridge: STUB — next session${X}" ;;
        21) echo -e "\n  ${D}FORGE: STUB — after Whorl v0.2${X}" ;;
        s|S) quick_syntax ;;
        t|T) launch_tree ;;
        u|U) cat "$ROOT/CONVERGENCE.md" 2>/dev/null | head -80 ;;
        g|G) grimoire ;;
        q|Q) 
            echo -e "\n  ${D}MotherBrain standing down.${X}"
            echo -e "  ${G}Go get Chew Plumbing.${X}\n"
            exit 0 ;;
        *)  echo -e "\n  ${D}Unknown command. Try again.${X}" ;;
    esac

    echo ""
    echo -e "  ${D}[press enter]${X}"
    read -r
done
