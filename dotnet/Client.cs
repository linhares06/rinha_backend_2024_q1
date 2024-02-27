using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ClientApi;

[Table("clients")]
public class Client
{
    [Column("id")]
    public int Id { get; set; }

    [Column("limite")]
    public int Limite { get; set; }

    [Column("saldo")]
    public int Saldo { get; set; }
}

[Table("transactions")]
public class Transaction
{
    [Column("id")]
    public int Id { get; set; }

    [Range(1, int.MaxValue, ErrorMessage = "Apenas inteiros positivos são permitidos.")]
    [Column("valor")]
    public int Valor { get; set; }

    [RegularExpression("^[cd]$", ErrorMessage = "Apenas 'c' para credito ou 'd' para debito permitido.")]
    [Column("tipo")]
    public char Tipo { get; set; }

    [Required]
    [StringLength(10, MinimumLength = 1, ErrorMessage = "Deve conter de 1 a 10 caracteres.")]
    [Column("descricao")]
    public string Descricao { get; set; } = null!;

    [DatabaseGenerated(DatabaseGeneratedOption.Computed)]
    [Column("realizada_em")]
    public DateTime RealizadaEm { get; set; }

    [Column("client_id")]
    public int ClientId { get; set; }
}
